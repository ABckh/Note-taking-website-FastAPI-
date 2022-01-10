function deleteNote(noteId){
    fetch("/del", {
        method: "POST",
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}