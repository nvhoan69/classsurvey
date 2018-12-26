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
    onclick="assess('${properties.id}')">Đánh giá</button>`,
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

function  assess(id) {
    window.location.href=`/student/assess/${id}`;
}
