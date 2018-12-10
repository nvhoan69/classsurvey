/*
global
alertify: false
call: false
fCall: false
fields: false
users: false
*/

const table = $('#table').DataTable(); // eslint-disable-line new-cap

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
    onclick="showUserModal('${properties.lecturer_id}')">Sửa</button>`,
    `<button type="button" class="btn btn-danger btn-xs"
    onclick="deleteUser('${properties.lecturer_id}')">Xóa</button>`
  );
  if (mode == 'edit') {
    table.row($(`#${properties.lecturer_id}`)).data(values);
  } else {
    const rowNode = table.row.add(values).draw(false).node();
    $(rowNode).attr('id', `${properties.lecturer_id}`);
  }
}

(function() {
  for (let i = 0; i < lecturers.length; i++) {
    addUser('create', lecturers[i]);
  }
})();

/**
 * Display user modal for creation.
 */
function showModal() { // eslint-disable-line no-unused-vars
  $('#edit-form').trigger('reset');
  $('#lecturer_id').val('')
  $('#title').text('Thêm mới giảng viên');
  $('#edit').modal('show');
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(lecturer_id) { // eslint-disable-line no-unused-vars
  call(`/admin/lecturer/get/${lecturer_id}`, function(properties) {
    for (const [property, value] of Object.entries(properties)) {
      $(`#${property}`).val(value);
    }
    $('#title').text(`Chỉnh sửa giảng viên ${properties.full_name}`);
    $('#edit').modal('show');
  });
}

function deleteUser(id) { // eslint-disable-line no-unused-vars
    call(`/admin/lecturer/get/${id}`, function (properties) {
        var full_name = properties.full_name
        var vnu_email = properties.vnu_email
        var account = properties.account
        $('#cf_full_name').text('Họ tên: ' + full_name)
        $('#cf_account').text('Tên tài khoản: ' + account)
        $('#cf_vnu_email').text('VNU email: ' + vnu_email)
    })
    $('#delete_confirm').modal('show');
    $('#doDelete').click(function () {
        doDelete(id);
    })
}

function doDelete(id) {
    call(`/admin/lecturer/delete/${id}`, function (success) {
        if(success=='Success') {
            $('#alert_message').text('Xóa thành công!')
            $('#alert').modal('show');
        }
    })
    $(`#${id}`).remove();
    $('#delete_confirm').modal('hide');
}
/**
* Create or edit lecturer.
*/
function processData() { // eslint-disable-line no-unused-vars
  fCall('/admin/lecturer/process_lecturer', '#edit-form', function(lecturer) {
    const title = $('#title').text().startsWith('Ch');
    const mode = title ? 'edit' : 'create';
    addUser(mode, lecturer);
    const message = `${mode == 'edit' ? 'Đã sửa' : 'Đã tạo'} giảng viên ${lecturer.full_name}. Tên tài khoản: ${lecturer.account}`;
    $('#alert_message').text(message);
    $('#alert').modal('show');
    $('#edit').modal('hide');
  });
}