import requests


class MailNavTasks:
    def __init__(self):
        self.url = 'https://fof.prism-advisor.com/api/v1/manager_mail/email_task'
        self.verify_token = ''

    def get_tasks(self):

        res = requests.post(
            url=self.url,
            data={
                'verify_token': self.verify_token,
            }
        )
        print(res.text)


if __name__ == '__main__':
    MailNavTasks().get_tasks()


