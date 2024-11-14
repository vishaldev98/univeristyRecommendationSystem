from base import db
from base.com.vo.universityinfo_vo import UniversityInfoVO


class UniversityInfoDAO:
    def insert_universityinfo(self, universityinfo_vo):
        db.session.add(universityinfo_vo)
        db.session.commit()

    def view_universityinfo(self):
        universityinfo_vo_list = UniversityInfoVO.query.all()
        return universityinfo_vo_list

    def delete_universityinfo(self, universityinfo_vo):
        universityinfo_vo_list = UniversityInfoVO.query.get(universityinfo_vo.universityinfo_id)
        db.session.delete(universityinfo_vo_list)
        db.session.commit()

    def edit_universityinfo(self, universityinfo_vo):
        universityinfo_vo_list = UniversityInfoVO.query \
            .filter_by(universityinfo_id=universityinfo_vo.universityinfo_id).all()
        return universityinfo_vo_list

    def update_universityinfo(self, universityinfo_vo):
        db.session.merge(universityinfo_vo)
        db.session.commit()
