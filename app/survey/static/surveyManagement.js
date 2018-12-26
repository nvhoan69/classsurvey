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

function  courseIndex() {
    window.location.href=`/survey/course/index`;
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(id) { // eslint-disable-line no-unused-vars
  call(`/survey/get/${id}`, function(properties) {
    var course_code = properties.course.course_code
    var course_name = properties.course.name
    var lecturer = properties.course.lecturer.full_name
    $('#info_course_code').text('Mã môn học: ' + course_code)
    $('#info_course_name').text('Tên môn học: ' + course_name)
    $('#info_lecturer').text('Giảng viên: ' + lecturer)

    for (const [property, value] of Object.entries(properties)) {
      if(property == 'title') {
          $('#survey_title').val(value);
      }
      else
          $(`#${property}`).val(value);
    }
    $('#title').text(`Chỉnh sửa cuộc khảo sát`);
    $('#edit').modal('show');
  });
}

function deleteUser(id) { // eslint-disable-line no-unused-vars
    call(`/survey/get/${id}`, function (properties) {
        var title = properties.survey_title
        var course_code = properties.course.course_code
        var course_name = properties.course.name
        var lecturer = properties.course.lecturer.full_name
        $('#cf_title').text('Tiêu đề: ' + title)
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
    call(`/survey/delete/${id}`, function (success) {
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
  fCall('/survey/process', '#edit-form', function(properties) {
    const title = $('#title').text().startsWith('Ch');
    const mode = title ? 'edit' : 'create';
    addUser(mode, properties);
    const message = `${mode == 'edit' ? 'Đã sửa' : 'Đã tạo'} cuộc khảo sát ${properties.survey_title}`;
    $('#alert_message').text(message);
    $('#alert').modal('show');
    $('#edit').modal('hide');
  });
}