from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.universityinfo_vo import UniversityInfoVO


class UniversityDetailsVO(db.Model):
    __tablename__ = 'universitydetails_table'
    universitydetails_id = db.Column('universitydetails_id', db.Integer, primary_key=True, autoincrement=True)
    universitydetails_cutoff = db.Column('universitydetails_cutoff', db.String(15), nullable=False)
    universitydetails_ielts_score = db.Column('universitydetails_ielts_score', db.String(15), nullable=False)
    universitydetails_gre_score = db.Column('universitydetails_gre_score', db.String(15), nullable=False)
    universitydetails_degree_id = db.Column('universitydetails_degree_id', db.Integer,
                                            db.ForeignKey(DegreeVO.degree_id))
    universitydetails_department_id = db.Column('universitydetails_department_id', db.Integer,
                                                db.ForeignKey(DepartmentVO.department_id))
    universitydetails_universityinfo_id = db.Column('universitydetails_universityinfo_id', db.Integer,
                                                    db.ForeignKey(UniversityInfoVO.universityinfo_id))

    def as_dict(self):
        return {
            'universitydetails_id': self.universitydetails_id,
            'universitydetails_cutoff': self.universitydetails_cutoff,
            'universitydetails_ielts_score': self.universitydetails_ielts_score,
            'universitydetails_gre_score': self.universitydetails_gre_score,
            'universitydetails_degree_id': self.universitydetails_degree_id,
            'universitydetails_department_id': self.universitydetails_department_id,
            'universitydetails_universityinfo_id': self.universitydetails_universityinfo_id
        }



