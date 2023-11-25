// CSRF PROTECTION
$.ajaxSetup({
    headers: { "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val() }
});

// Global Search
let searchQuery = ''


// BOOKSHELF TAB / CARDS
$(document).ready(function() {
    $("#bookshelfLink").click(function(event) {
        event.preventDefault();
        $("#library").hide();
        $.ajax({
            url: '/booklibrary/get-user-bookshelf/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                var content = '';
                $.each(data, function (index, book) {
                    content += `
                    <a href="#" class="card-link"
                       data-book-id="${book.id}" 
                       data-title="${book.title}"
                       data-author="${book.author}"
                       data-year="${book.published_year}"
                       data-genre="${book.genre}"
                       data-pages="${book.pages}"
                       data-description="${book.description}"
                       data-thumbnail="${book.thumbnail}"
                       data-ratings_avg="${book.ratings_avg}"
                       data-ratings_count="${book.ratings_count}"
                       data-isbn10="${book.isbn10}" 
                       data-isbn13="${book.isbn13}" 
                       data-source="bookshelf"
                       data-status="${book.status}">
                        <div class="card item">
                            <img src="${book.thumbnail}" class="card-img-top" alt="a book">
                            <div class="card-body">
                                <h5 class="card-title">${book.title}</h5>
                                <p class="card-text" data-status-id="${book.id}">Status: ${book.status}</p>
                            </div>
                        </div>
                    </a>`;
                });
                $("#bookshelf").html(content).show();
            },
            error: function (error) {
                console.error("Error fetching bookshelf:", error);
            }
        });
    });

    $("#libraryLink").click(function (event) {
        event.preventDefault();
        $("#bookshelf").hide();
        $("#library").show();
    });
});

// ==================================================================

// MODAL CARDS
$(document).on('click', '.card-link', function() {
    const bookId = $(this).data('book-id');
    const title = $(this).data('title');
    const author = $(this).data('author');
    const year = $(this).data('year');
    const genre = $(this).data('genre');
    const pages = $(this).data('pages');
    const description = $(this).data('description');
    const thumbnail = $(this).data('thumbnail');
    const ratings_avg = $(this).data('ratings_avg');
    const ratings_count = $(this).data('ratings_count');
    const isbn10 = $(this).data('isbn10');
    const isbn13 = $(this).data('isbn13');
    const source = $(this).data('source');
    const bookStatus = $(this).data('status'); 

    // Now populate the modal with these values
    $("#modalBookTitle").text(title);
    $('#modalBookThumbnail').attr('src', thumbnail);
    $("#modalBookGenreYear").text(genre + " | " + year);
    $("#modalBookAuthor").text(author);
    $("#modalBookPages").text(pages);
    $("#modalBookDescription").text(description);
    $("#modalBookAvgRate").text(ratings_avg);
    $("#modalBookCountRate").text(ratings_count);
    $("#modalBookIsbn10").text(isbn10);
    $("#modalBookIsbn13").text(isbn13);

    // Buttons
    $('#buyOnAmazonButton').attr('href', `https://www.amazon.com/s?k=${isbn13}`);
    $('#borrowReadButton').data('book-id', bookId);

    // Check the source and adjust the button text
    if(source === 'library') {
        $('#borrowReadButton').text('Borrow/Read'); //set Text
        $('#borrowReadButton').attr('class', 'btn btn-primary borrowRead'); //set Button's Class
    } else if(source === 'bookshelf') {
        // If-else status condition here
        if(bookStatus === 'Completed') {
            $('#borrowReadButton').text('Re-read Book');
            $('#borrowReadButton').attr('class', 'btn btn-info reRead');
        } else {
            $('#borrowReadButton').text('Complete Reading');
            $('#borrowReadButton').attr('class', 'btn btn-success completeReading');
        }
    }

    // Finally, display the modal
    $("#bookDetailsModal").modal('show');
});

// ==================================================================

// BORROW/READ FEATURE
function showNotificationSuccess() {
    $('#notificationSuccess').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }
function showNotificationFailed() {
    $('#notificationFailed').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }

$(document).on('click', '.borrowRead', function(event) {
    event.preventDefault();
    let bookId = $(this).data('book-id');
    $.ajax({
        url: '/booklibrary/borrow-book/', 
        method: 'POST',
        data: {
            'book_id': bookId,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response.status === 'success') {
                window.scrollTo(0, 0);
                showNotificationSuccess();
                $('#bookDetailsModal').modal('hide');

            } else {
                window.scrollTo(0, 0);
                showNotificationFailed();
                $('#bookDetailsModal').modal('hide');
            }
        },
        error: function() {
            alert('An error occurred. Please try again.');
        }
    });
});

// ==================================================================

// COMPLETE READING FEATURE
function showReadingSuccess() {
    $('#readingSuccess').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }
function showReadingFailed() {
    $('#readingFailed').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }
$(document).on('click', '.completeReading', function(event) {
    event.preventDefault();
    let bookId = $(this).data('book-id');
    $.ajax({
        url: '/booklibrary/complete-reading/', // Update the URL based on your Django URL structure
        method: 'POST',
        data: {
            'book_id': bookId,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {

            if (response.status === 'success') {
                $(`[data-status-id="${bookId}"]`).text('Status: Completed');
                // Update the modal button
                $('#borrowReadButton').text('Re-read Book');
                $('#borrowReadButton').attr('class', 'btn btn-info reRead');
                // Update the status data attribute for the card link
                $(`.card-link[data-book-id="${bookId}"]`).data('status', 'Completed');
                window.scrollTo(0, 0);
                showReadingSuccess();
                $('#bookDetailsModal').modal('hide');

            } else {
                window.scrollTo(0, 0);
                showReadingFailed();
                $('#bookDetailsModal').modal('hide');
            }
        },
        error: function() {
            alert('An error occurred. Please try again.');
        }
    });
});

// ==================================================================

// RE-READING FEATURE
function showReReadingSuccess() {
    $('#reReadingSuccess').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }
function showReReadingFailed() {
    $('#reReadingFailed').show().delay(3000).fadeOut(); // This will display the notification and hide it after 5 seconds.
  }
$(document).on('click', '.reRead', function(event) {
    event.preventDefault();
    let bookId = $(this).data('book-id');
    $.ajax({
        url: '/booklibrary/re-read-book/', // Update the URL based on your Django URL structure
        method: 'POST',
        data: {
            'book_id': bookId,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {

            if (response.status === 'success') {
                $(`[data-status-id="${bookId}"]`).text('Status: Currently Reading');
                $(`[data-status-id="${bookId}"]`).text('Status: Currently Reading');
                // Update the modal button
                $('#borrowReadButton').text('Complete Reading');
                $('#borrowReadButton').attr('class', 'btn btn-success completeReading');
                // Update the status data attribute for the card link
                $(`.card-link[data-book-id="${bookId}"]`).data('status', 'Reading');
                window.scrollTo(0, 0);
                $('#bookDetailsModal').modal('hide');
                showReReadingSuccess();

            } else {
                window.scrollTo(0, 0);
                showReReadingFailed();
                $('#bookDetailsModal').modal('hide');
            }
        },
        error: function() {
            alert('An error occurred. Please try again.');
        }
    });
});

// ==================================================================

// Tangkap event submit form pencarian
// $("#search_book").submit(function (event) {
//     event.preventDefault(); // Hindari form dari proses submit bawaan browser

//     searchQuery = $("#search_bar").val(); // Ambil nilai dari input pencarian

//     // Kirim permintaan Ajax dengan kata kunci pencarian dan nomor halaman
//     loadBooks(searchQuery);
// });

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Prevent Submit Button
$("#search_book").submit(function(event) {
    event.preventDefault(); // just prevent the default submit behavior
});

$("#search_bar").on('keyup', debounce(function() {
    const searchQuery = $(this).val();
    loadBooks(searchQuery);
}, 100));  // The search will be triggered after 300ms of the user stopping typing

function loadBooks(searchQuery) {
    $.ajax({
        type: "POST",
        url: "load-books/",
        data: {
            search_query: searchQuery,
        },
        success: function (response) {
            if (response.status === "success") {
                // Update daftar buku di antarmuka pengguna dengan data yang diterima
                const booksContainer = $("#library");
                booksContainer.empty(); // Kosongkan daftar buku sebelum memasukkan buku yang baru dimuat
                $.each(JSON.parse(response.books), function (index, book) {
                    // Tambahkan buku ke daftar buku
                    booksContainer.append(`<a
                    href="#"
                    class="card-link"
                    data-book-id="${book.pk}"
                    data-title="${book.fields.title}"
                    data-author="${book.fields.author}"
                    data-year="${book.fields.published_year}"
                    data-genre="${book.fields.genre}"
                    data-pages="${book.fields.pages}"
                    data-description="${book.fields.description}"
                    data-thumbnail="${book.fields.thumbnail}"
                    data-ratings_avg="${book.fields.ratings_avg}"
                    data-ratings_count="${book.fields.ratings_count}"
                    data-isbn10="${book.fields.isbn10}"
                    data-isbn13="${book.fields.isbn13}"
                    data-source="library"
                    data-status="not-started"
                    data-review-url="book/${book.fields.isbn13}/review/"
                    >
                        <div class="card item border-secondary" data-book-id="${book.pk}">
                        <img src="${book.fields.thumbnail}" class="card-img-top" alt="a book" />
                        <div class="card-body">
                            <h5 class="card-title" id="title">${book.fields.title}</h5>
                            <p class="card-text" id="year">${book.fields.author}</p>
                        </div>
                        </div>
                    </a>`);
                });
            } else {
                console.log(response.message);
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        },
    });
}

$(document).ready(function() {
    loadBooks(searchQuery);
});