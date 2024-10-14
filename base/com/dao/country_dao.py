from base import db
from base.com.vo.country_vo import CountryVO


class CountryDAO:
    def insert_country(self, country_vo):
        db.session.add(country_vo)
        db.session.commit()

    def view_country(self):
        country_vo_list = CountryVO.query.all()
        return country_vo_list

    def delete_country(self, country_vo):
        country_vo_list = CountryVO.query.get(country_vo.country_id)
        db.session.delete(country_vo_list)
        db.session.commit()

    def edit_country(self, country_vo):
        country_vo_list = CountryVO.query. \
            filter_by(country_id=country_vo.country_id).all()
        return country_vo_list

    def update_country(self, country_vo):
        db.session.merge(country_vo)
        db.session.commit()
