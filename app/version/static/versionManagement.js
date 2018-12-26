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
      let value = properties[fields[i]];
      if(value == true){
          value = 'Mặc định';
      }
      if(value == false){
          value = 'Không';
      }
      values.push(`${value}`);
  }
  values.push(
    `<button type="button" class="btn btn-info btn-xs"
    onclick="showUserModal('${properties.id}')">Sửa</button>`,
    `<button type="button" class="btn btn-danger btn-xs"
    onclick="deleteUser('${properties.id}')">Xóa</button>`,
    `<button type="button" class="btn btn-info btn-xs"
    onclick="setDefault('${properties.id}')">Đặt mặc định</button>`,
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

function  courseIndex() {
    window.location.href=`/survey/course/index`;
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(id) { // eslint-disable-line no-unused-vars
  call(`/version/get/${id}`, function(properties) {
    for (const [property, value] of Object.entries(properties)) {
        $(`#${property}`).val(value);
    }
    $('#title').text(`Chỉnh sửa tên mẫu phiếu`);
    $('#edit').modal('show');
  });
}

function deleteUser(id) { // eslint-disable-line no-unused-vars
    call(`/version/get/${id}`, function (properties) {
        var name = properties.name
        var is_default
        if(properties.is_default == true) {
            is_default = 'Mặc định';
        }
        else is_default = 'Không';
        $('#cf_version_name').text('Tên mẫu: ' + name)
        $('#cf_is_default').text('Mặc định: ' + is_default)
    })
    $('#delete_confirm').modal('show');
    $('#doDelete').unbind("click");
    $('#doDelete').click(function () {
        doDelete(id);
    })
}

function doDelete(id) {
    call(`/version/delete/${id}`, function (success) {
        if(success=='Success') {
            $('#alert_message').text('Xóa thành công!')
            $('#alert').modal('show');
        }
    })
    $(`#${id}`).remove();
    $('#delete_confirm').modal('hide');
}
/**
* Edit
*/
function processData() { // eslint-disable-line no-unused-vars
  fCall('/version/process', '#edit-form', function(properties) {
    if(properties == 'false') {
        const message = 'Tác vụ không thành công!';
        $('#alert_message').text(message);
        $('#alert').modal('show');
        $('#edit').modal('hide');
    }
    else {
        const title = $('#title').text().startsWith('Ch');
        const mode = title ? 'edit' : 'create';
        addUser(mode, properties);
        const message = `${mode == 'edit' ? 'Đã sửa' : 'Đã tạo'} mẫu phiếu khảo sát ${properties.name}`;
        $('#alert_message').text(message);
        $('#alert').modal('show');
        $('#edit').modal('hide');
    }
  });
}

function setDefault(id) { // eslint-disable-line no-unused-vars
    call(`/version/get/${id}`, function (properties) {
        var name = properties.name
        var is_default
        if(properties.is_default == true) {
            is_default = 'Mặc định';
        }
        else is_default = 'Không';
        $('#cf_df_version_name').text('Tên mẫu: ' + name)
        $('#cf_df_is_default').text('Mặc định: ' + is_default)
    })
    $('#set_default_confirm').modal('show');
    $('#doSetDefault').unbind("click");
    $('#doSetDefault').click(function () {
        doSetDefault(id);
    })
}

function doSetDefault(id) {
    window.location.href=`/version/set_default/${id}`;
}