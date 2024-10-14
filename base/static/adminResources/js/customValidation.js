/*###########################
#########Add Country##########
############################*/
function addCountry() {

    if ($('#countryName').val().trim() === '') {
        $('#countryName').focus()
        showErrorToast('Please Enter Country Name')
        return false;
    } else if ($('#countryName').val().length < 3) {
        $('#countryName').focus()
        showErrorToast('Please Enter Valid Country Name')
        return false;
    } else if ($('#countryDescription').val().trim() === '') {
        $('#countryDescription').focus()
        showErrorToast('Please Enter Country Description')
        return false;
    } else {
        return true;
    }
}


/*###########################
#########Add Degree##########
############################*/

function addDegree() {

    if ($('#degreeName').val().trim() === '') {
        $('#degreeName').focus()
        showErrorToast('Please Enter Degree Name')
        return false;
    } else if ($('#degreeName').val().length < 2) {
        $('#degreeName').focus()
        showErrorToast('Please Enter Valid Degree Name')
        return false;
    } else if ($('#degreeDescription').val().trim() === '') {
        $('#degreeDescription').focus()
        showErrorToast('Please Enter Degree Description')
        return false;
    } else {
        return true;
    }
}



/*###########################
#########Add Department##########
############################*/

function addDepartment() {

    if ($('#departmentDegreeId').val() == 'none') {
        $('#departmentDegreeId').focus()
        showErrorToast('Please select valid Degree Name')
        return false;
    } else if ($('#departmentName').val().length < 2) {
        $('#departmentName').focus()
        showErrorToast('Please Enter Department Name')
        return false;
    } else if ($('#departmentDescription').val().trim() === '') {
        $('#departmentDescription').focus()
        showErrorToast('Please Enter Department Description')
        return false;
    } else {
        return true;
    }
}