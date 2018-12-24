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
      if(fields[i] == 'lecturer') {
          values.push(`${properties[fields[i]].full_name}`);
      }
      else {
          values.push(`${properties[fields[i]]}`);
      }

  }
  values.push(
    `<button id="student_index" type="button" class="btn btn-info btn-xs"
    onclick="studentIndex('${properties.id}')">Danh sách sinh viên</button>`,
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

function  studentIndex(id) {
    window.location.href=`/course/student/index/${id}`;
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(id) { // eslint-disable-line no-unused-vars
  call(`/course/get/${id}`, function(properties) {
    for (const [property, value] of Object.entries(properties)) {
      $(`#${property}`).val(value);
    }
    $('#title').text(`Chỉnh sửa lớp môn học ${properties.name}`);
    $('#edit').modal('show');
  });
}

function deleteUser(id) { // eslint-disable-line no-unused-vars
    call(`/course/get/${id}`, function (properties) {
        var course_code = properties.course_code
        var course_name = properties.name
        var lecturer = properties.lecturer.full_name
        $('#cf_course_code').text('Mã môn học: ' + course_code)
        $('#cf_course_name').text('Tên môn học: ' + course_name)
        $('#cf_lecturer').text('Giảng viên: ' + lecturer)
    })
    $('#delete_confirm').modal('show');
    $('#doDelete').unbind("click");
    $('#doDelete').click(function () {
        doDelete(id);
    })
}

function doDelete(id) {
    call(`/course/delete/${id}`, function (success) {
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
  fCall('/course/process', '#edit-form', function(properties) {
    const title = $('#title').text().startsWith('Ch');
    const mode = title ? 'edit' : 'create';
    addUser(mode, properties);
    const message = `${mode == 'edit' ? 'Đã sửa' : 'Đã tạo'} lớp môn học ${properties.name}. Mã môn học: ${properties.course_code}`;
    $('#alert_message').text(message);
    $('#alert').modal('show');
    $('#edit').modal('hide');
  });
}