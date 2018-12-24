/*
global
alertify: false
call: false
fCall: false
fields: false
users: false
*/

const table = $('#table').DataTable({
    language: {
        url: '/static/build/language/Vietnamese.json'
    }
}); // eslint-disable-line new-cap

/**
 * Add user to datatable or edit line.
 * @param {mode} mode - Create or edit.
 * @param {properties} properties - Properties of the user.
 */
function addUser(mode, properties) {

  let values = [];
  for (let i = 0; i < fields.length; i++) {
    values.push(`${properties[fields[i]]}`);
  }
  values.push(
    `<button type="button" class="btn btn-info btn-xs"
    onclick="showUserModal('${properties.id}')">Sửa</button>`,
    `<button type="button" class="btn btn-danger btn-xs"
    onclick="deleteUser('${properties.id}')">Xóa</button>`
  );
  if (mode == 'edit') {
    table.row($(`#${properties.id}`)).data(values);
  } else {
    const rowNode = table.row.add(values).draw(false).node();
    $(rowNode).attr('id', `${properties.id}`);
  }
}

(function() {
  for (let i = 0; i < users.length; i++) {
    addUser('create', users[i]);
  }
})();

/**
 * Display user modal for creation.
 */
function showModal() { // eslint-disable-line no-unused-vars
  $('#edit-form').trigger('reset');
  $('#student_id').val('')
  $('#title').text('Thêm mới sinh viên');
  $('#edit').modal('show');
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(id) { // eslint-disable-line no-unused-vars
  call(`/student_mn/get/${id}`, function(properties) {
    for (const [property, value] of Object.entries(properties)) {
      $(`#${property}`).val(value);
    }
    $('#title').text(`Chỉnh sửa sinh viên ${properties.full_name}`);
    $('#edit').modal('show');
  });
}

function deleteUser(id) { // eslint-disable-line no-unused-vars
    call(`/student_mn/get/${id}`, function (properties) {
        var full_name = properties.full_name
        var vnu_email = properties.vnu_email
        var student_code = properties.student_code
        var class_course = properties.class_course
        $('#cf_full_name').text('Họ tên: ' + full_name)
        $('#cf_student_code').text('Mã sinh viên: ' + student_code)
        $('#cf_vnu_email').text('VNU email: ' + vnu_email)
        $('#cf_class_course').text('Khóa đào tạo: ' + class_course)
    })
    $('#delete_confirm').modal('show');
    $('#doDelete').unbind("click");
    $('#doDelete').click(function () {
        doDelete(id);
    })
}

function doDelete(id) {
    call(`/student_mn/delete/${id}`, function (success) {
        if(success=='Success') {
            $('#alert_message').text('Xóa thành công!')
            $('#alert').modal('show');
        }
    })
    $(`#${id}`).remove();
    $('#delete_confirm').modal('hide');
}

/**
* Create or edit user.
*/
function processData() { // eslint-disable-line no-unused-vars
  fCall('/student_mn/process', '#edit-form', function(student) {
    const title = $('#title').text().startsWith('Ch');
    const mode = title ? 'edit' : 'create';
    addUser(mode, student);
    const message = `${mode == 'edit' ? 'Đã sửa' : 'Đã tạo'} sinh viên ${student.full_name}. Mã sinh viên: ${student.student_code}`;
    $('#alert_message').text(message);
    $('#alert').modal('show');
    $('#edit').modal('hide');
  });
}