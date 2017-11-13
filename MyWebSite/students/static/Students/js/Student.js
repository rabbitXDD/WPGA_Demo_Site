var scrollLock = false;

function loadStudents(url, paginationfield, load) {
    if (scrollLock === true) {
        return false;
    }
    page = parseInt($(paginationfield).val()) + 1;
    
    $(load).text("Loading ...");
    data = {page: page};

    $.get(url, data, function(data) {
        $.each(data, function(index, ele) {
            if (ele.grade.length !== 0) {
                $.each(ele.grade, function(index, grade) {
                    if (index === 0) {
                        $('#content tbody#studentsTable').append( 
                            "<tr>" +
                            "<td>" + ele.firstName + "</td>" +
                            "<td>" + ele.lastName + "</td>" +
                            "<td>" + ele.phoneNumber + "</td>" +
                            "<td>" + grade.examNumber + "</td>" +
                            "<td>" + grade.subject1Score + "</td>" +
                            "<td>" + grade.subject2Score + "</td>" +
                            "<td>" + grade.subject3Score + "</td>" +
                            "<tr>"  
                        );
                    } else {
                        $('#content tbody#studentsTable').append( 
                            "<tr>" +
                            "<td></td>" +
                            "<td></td>" +
                            "<td></td>" +
                            "<td>" + grade.examNumber + "</td>" +
                            "<td>" + grade.subject1Score + "</td>" +
                            "<td>" + grade.subject2Score + "</td>" +
                            "<td>" + grade.subject3Score + "</td>" +
                            "<tr>"  
                        );
                    }
                });
            } else {
                $('#content tbody#studentsTable').append( 
                    "<tr>" +
                    "<td>" + ele.firstName + "</td>" +
                    "<td>" + ele.lastName + "</td>" +
                    "<td>" + ele.phoneNumber + "</td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<tr>"  
                );
            }
        });
        $(paginationfield).val(page + 1);
        $(window).scroll(scrollHandler);
    }, 
    "json").fail(function() {
        $(load).replaceWith("<p>No more data</p>");
        scrollLock = true;
    });
}

var scrollHandler = function() {
    $('#top').text(jQuery(this).scrollTop());
    myScroll = $(window).scrollTop();

    if(myScroll > $(document).height() - ($(window).height() * 2)) {
        loadStudents(
            "/students/pagination/ajax/_scroll/",
            "#pagination",
            "#load"
        );
        $(window).off('scroll', scrollHandler); 
    }
};

$(document).ready(function() {
    $(window).scroll(scrollHandler);
    loadStudents(
        "/students/pagination/ajax/_scroll/",
        "#pagination"
    );

    $(function(){
      // bind change event to select
      $('#pageSelect').on('change', function () {
          var url = $(this).val(); // get selected value
          if (url) { // require a URL
              window.location = url; // redirect
          }
          return false;
      });
    });
});
