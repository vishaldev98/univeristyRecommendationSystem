from base import db
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.department_vo import DepartmentVO


class DepartmentDAO:
    def insert_department(self, department_vo):
        db.session.add(department_vo)
        db.session.commit()

    def view_department(self):
        department_vo_list = db.session.query(DepartmentVO, DegreeVO) \
            .join(DegreeVO, DepartmentVO.department_degree_id == DegreeVO.degree_id) \
            .all()
        return department_vo_list

    def delete_department(self, department_id):
        department_vo_list = DepartmentVO.query.get(department_id)
        db.session.delete(department_vo_list)
        db.session.commit()

    def edit_department(self, department_vo):
        department_vo_list = DepartmentVO.query.filter_by(department_id=department_vo.department_id).all()
        return department_vo_list

    def update_department(self, department_vo):
        db.session.merge(department_vo)
        db.session.commit()

    def view_ajax_department_universitydetails(self, department_vo):
        department_vo_list = DepartmentVO.query.filter_by(
            department_degree_id=department_vo.department_degree_id).all()
        return department_vo_list
