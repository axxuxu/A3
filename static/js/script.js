function toggleRequestForm(button, grade_id){
  const requestRow = document.getElementById('request-row-' + grade_id);
  if (requestRow.style.display == 'none'){
    requestRow.style.display = 'table-row'; // show row
  } else {
    requestRow.style.display = 'none'; // hide row
  }
}

$(document).ready(function() {
  $('.reason-input').off('keydown').on('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      event.stopPropagation();
      const gradeId = $(this).attr('grade_id');
      const reason = $('#reason-' + gradeId).val();
      const requestRow = document.getElementById('request-row-' + gradeId);

      if (!reason.trim()) {
        alert('Please provide a reason for the remark request.');
        return;
      }
      req = $.ajax({
        url: '/submit-request',
        type: 'POST',
        data: { gradeId: gradeId, reason: reason }
      })
  
      req.done(function(){
        $('#reason-' + gradeId).val('');  
        requestRow.style.display = 'none';      
        $('#status-'+gradeId).text('Pending');
        alert("Remark request submitted successfully!", "success");
      })
    }
  });

  $('.submit-request').off('click').on('click',function() {
    const gradeId = $(this).attr('grade_id');
    const reason = $('#reason-' + gradeId).val();
    const requestRow = document.getElementById('request-row-' + gradeId);

    if (!reason.trim()) {
      alert('Please provide a reason for the remark request.');
      return;
    }
    req = $.ajax({
      url: '/submit-request',
      type: 'POST',
      data: { gradeId: gradeId, reason: reason }
      
    })

    req.done(function(){
      $('#reason-' + gradeId).val(''); 
      requestRow.style.display = 'none';      
      $('#status-'+gradeId).text('Pending'); 
      alert("Remark request submitted successfully!", "success");
    })
  });

  $('.accept-btn').on('click', function() {
    const gradeId = $(this).attr('gradeId');
    const requestId = $(this).attr('requestId');
    req = $.ajax({
      url: '/change-status',
      type: 'POST',
      data: {requestId: requestId, gradeId: gradeId, new_status: 'Accepted'}
    })

    req.done(function(){
      $('#status-' + requestId).text('Accepted'); 
    })

  });

  $('.reject-btn').on('click', function() {
    const gradeId = $(this).attr('gradeId');
    const requestId = $(this).attr('requestId');
    req = $.ajax({
      url: '/change-status',
      type: 'POST',
      data: {requestId: requestId, gradeId: gradeId, new_status: 'Rejected'}
    })

    req.done(function(){
      $('#status-' + requestId).text('Rejected');
    })

  });
});

// instructor_grades refresh
document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector(".grade-table")) { 
    fetchGrades();
    setInterval(fetchGrades, 5000);
  };
});

function fetchGrades() {
  $.ajax({
    url: "/instructor_grades",
    type: "GET",
    dataType: "json",
    success: function(data) {
      let tableBody = $(".grade-table tbody");
      tableBody.empty();

      $.each(data, function(index, student) {
        let row = `<tr>
          <td>${student.utorid}</td>
          <td>${student.lastname}</td>
          <td>${student.firstname}</td>
          <td>${student.A1 !== null ? student.A1 + "%" : "N/A"}</td>
          <td>${student.A2 !== null ? student.A2 + "%" : "N/A"}</td>
          <td>${student.A3 !== null ? student.A3 + "%" : "N/A"}</td>
          <td>${student.Labs !== null ? student.Labs + "%" : "N/A"}</td>
          <td>${student.Midterm !== null ? student.Midterm + "%" : "N/A"}</td>
          <td>${student.Final !== null ? student.Final + "%" : "N/A"}</td>
        </tr>`;
        tableBody.append(row);
      });
    },
    error: function(error) {
      console.error("Error fetching grades:", error);
    }
  });
}

setInterval(fetchGrades, 5000);

$(document).ready(function() {
  fetchGrades();
});
//changes end
