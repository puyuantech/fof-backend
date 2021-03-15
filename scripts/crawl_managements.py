
import datetime
import multiprocessing.dummy as mp
import pathlib
import traceback

from flask import current_app
from functools import partial
from pydantic import ValidationError

from bases.exceptions import NotFoundError
from bases.globals import db
from extensions.manager.spider import ManagementSpider
from extensions.manager.validator import ManageFundValidation
from models import ManagementFund


def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log_message(path, message):
    with open(path, 'a') as f:
        f.write(message + '\n')


class ManagementCrawler:

    def __init__(self):
        self.path = pathlib.Path(__file__).parent.absolute() / 'managements'
        self.error_exceptions_path = self.path / 'error_exceptions.log'
        self.error_funds_path = self.path / 'error_funds.log'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.funds = {}

    def setup_proxy(self, username, password):
        host, port = 'dyn.horocn.com', 50000
        proxy = f'http://{username}:{password}@{host}:{port}'
        self.proxies = {
            'http': proxy,
            'https': proxy,
        }

    def load_funds(self):
        funds = db.session.query(
            ManagementFund.fund_id,
            ManagementFund.fund_name,
            ManagementFund.update_date,
        ).filter_by(is_deleted=False).all()
        self.funds = [(fund.fund_id, fund.fund_name, fund.update_date) for fund in funds]
        current_app.logger.info(f'[load_funds][{now_time()}] done! (len){len(self.funds)}')

    def crawl_fund(self, fund_info, app):
        fund_id, fund_name, update_date = fund_info
        with app.app_context():
            retry = 0
            while retry < 3:
                if retry > 0:
                    current_app.logger.warning(f'[update_fund_info][{now_time()}] Retry {retry} times (fund_id){fund_id}')

                try:
                    fund_info = ManagementSpider.get_fund_info(fund_id, self.proxies)
                    fund_info_validation = ManageFundValidation.get_fund(fund_info)

                    if fund_name is None or update_date != fund_info_validation.update_date:
                        fund = db.session.query(ManagementFund).get(fund_id)
                        fund.update(**fund_info_validation.dict())
                    return True

                except NotFoundError:
                    fund = db.session.query(ManagementFund).get(fund_id)
                    fund.logic_delete()
                    return True

                except ValidationError:
                    err_msg = f'[update_fund_info][{now_time()}] failed! (fund_id){fund_id} (fund_info){fund_info} (err_msg){traceback.format_exc()}'
                    current_app.logger.error(err_msg)
                    log_message(self.error_exceptions_path, err_msg)
                    log_message(self.error_funds_path, str(fund_id))
                    return False

                except Exception:
                    retry += 1
                    if retry > 2:
                        err_msg = f'[update_fund_info][{now_time()}] failed! (fund_id){fund_id} (err_msg){traceback.format_exc()}'
                        current_app.logger.error(err_msg)
                        log_message(self.error_exceptions_path, err_msg)
                        log_message(self.error_funds_path, str(fund_id))

            return False

    def parallel_craw_funds(self):
        self.load_funds()

        p = mp.Pool(5)
        p.map(partial(self.crawl_fund, app=current_app._get_current_object()), self.funds)
        p.close()
        p.join()

