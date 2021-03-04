from typing import List

from bases.constants import UserRiskLevel
from bases.dbwrapper import db, BaseModel


class RiskQuestion(BaseModel):
    """风险测评问题"""
    __tablename__ = 'risk_questions'

    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.Integer)    # 编号
    question = db.Column(db.String(128)) # 问题
    symbol = db.Column(db.JSON)          # 答案选项: ["A", "B", ...]
    answer = db.Column(db.JSON)          # 答案: ["18-30岁", "31-50岁", ...]
    score = db.Column(db.JSON)           # 得分: [1, 3, ...]

    @staticmethod
    def get_risk_level_by_score(score):
        if score <= 20:
            return UserRiskLevel.保守型
        if score <= 40:
            return UserRiskLevel.稳健型
        if score <= 60:
            return UserRiskLevel.平衡型
        if score <= 80:
            return UserRiskLevel.成长型
        return UserRiskLevel.进取型

    @classmethod
    def get_questions(cls):
        return cls.filter_by_query().order_by(cls.order_num).all()

    @classmethod
    def calc_risk_score(cls, answers: List[str]) -> int:
        risk_score = 0
        questions = cls.filter_by_query().order_by(cls.order_num).all()
        for question, answer in zip(questions, answers):
            for symbol, score in zip(question.symbol, question.score):
                if symbol == answer:
                    risk_score += score
                    break
        return risk_score


class RiskAnswer(BaseModel):
    """风险测评结果"""
    __tablename__ = 'risk_answers'

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.String(32))
    risk_level = db.Column(db.String(4))     # 风险承受能力: C1 ~ C5
    risk_level_score = db.Column(db.Integer) # 风险测评得分
    risk_level_answers = db.Column(db.JSON)  # 答案: ["A", "A", ...]

