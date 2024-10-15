from flask import request, render_template, redirect

from base import app
from base.com.dao.country_dao import CountryDAO
from base.com.vo.country_vo import CountryVO


@app.route('/admin/load_country', methods=['GET'])
def admin_load_country():
    try:
        return render_template('admin/addCountry.html')
    except Exception as ex:
        print("admin_load_country route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/insert_country', methods=['POST'])
def admin_insert_country():
    try:
        country_name = request.form.get('countryName')
        country_description = request.form.get('countryDescription')

        country_vo = CountryVO()
        country_dao = CountryDAO()

        country_vo.country_name = country_name
        country_vo.country_description = country_description
        country_dao.insert_country(country_vo)
        return redirect('/admin/view_country')

    except Exception as ex:
        print("admin_insert_country route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/view_country', methods=['GET'])
def admin_view_country():
    try:
        country_dao = CountryDAO()
        country_vo_list = country_dao.view_country()
        return render_template('admin/viewCountry.html', country_vo_list=country_vo_list)

    except Exception as ex:
        print("admin_view_country route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/delete_country', methods=['GET'])
def admin_delete_country():
    try:
        country_vo = CountryVO()
        country_dao = CountryDAO()

        country_id = request.args.get('countryId')
        print("In delete country>>>>>>>>>>>>>>", country_id)
        country_vo.country_id = country_id
        country_dao.delete_country(country_vo)
        return redirect('/admin/view_country')

    except Exception as ex:
        print("admin_delete_country route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/edit_country', methods=['GET'])
def admin_edit_country():
    try:
        country_vo = CountryVO()
        country_dao = CountryDAO()

        country_id = request.args.get('countryId')
        country_vo.country_id = country_id
        country_vo_list = country_dao.edit_country(country_vo)
        print("in admin_edit_country country_vo_list>>>>>>", country_vo_list)
        print("in admin_edit_country type of country_vo_list>>>>>>>", type(country_vo_list))
        return render_template('admin/editCountry.html', country_vo_list=country_vo_list)

    except Exception as ex:
        print("admin_edit_country route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/update_country', methods=['POST'])
def admin_update_country():
    try:
        country_id = request.form.get('countryId')
        country_name = request.form.get('countryName')
        country_description = request.form.get('countryDescription')

        country_vo = CountryVO()
        country_dao = CountryDAO()

        country_vo.country_id = country_id
        country_vo.country_name = country_name
        country_vo.country_description = country_description
        country_dao.update_country(country_vo)
        return redirect('/admin/view_country')

    except Exception as ex:
        print("admin_update_country route exception occurred>>>>>>>>>>", ex)