from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.universitydetails_vo import UniversityDetailsVO
from base.com.vo.universityinfo_vo import UniversityInfoVO


class UniversityDetailsDAO:
    def insert_universitydetails(self, universitydetails_vo):
        db.session.add(universitydetails_vo)
        db.session.commit()

    def view_universitydetails(self):
        universitydetails_vo_list = db.session.query(DegreeVO, DepartmentVO, UniversityInfoVO,
                                                     UniversityDetailsVO).filter(
            DegreeVO.degree_id == UniversityDetailsVO.universitydetails_degree_id).filter(
            DepartmentVO.department_id == UniversityDetailsVO.universitydetails_department_id).filter(
            UniversityInfoVO.universityinfo_id == UniversityDetailsVO.universitydetails_universityinfo_id).all()

        return universitydetails_vo_list

    def delete_universitydetails(self, universitydetails_vo):
        universitydetails_vo_list = UniversityDetailsVO.query.get(universitydetails_vo.universitydetails_id)
        db.session.delete(universitydetails_vo_list)
        db.session.commit()

    def edit_universitydetails(self, universitydetails_vo):
        universitydetails_vo_list = UniversityDetailsVO.query. \
            filter_by(universitydetails_id=universitydetails_vo.universitydetails_id).all()
        return universitydetails_vo_list

    def update_universitydetails(self, universitydetails_vo):
        db.session.merge(universitydetails_vo)
        db.session.commit()
