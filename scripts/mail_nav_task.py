import requests


class MailNavTasks:
    def __init__(self):
        # self.login_url = 'https://fof.prism-advisor.com/api/v1/manager_mail/email_task'
        self.login_url = 'http://127.0.0.1:8005/api/v1/manager_mail/email_task'
        self.verify_token = 'jisn401f7ac837da42b97f613d789819f37bee6a'

    def get_tasks(self):

        res = requests.post(
            url=self.login_url,
            data={
                'verify_token': self.verify_token,
            }
        )
        print(res.text)


if __name__ == '__main__':
    MailNavTasks().get_tasks()


