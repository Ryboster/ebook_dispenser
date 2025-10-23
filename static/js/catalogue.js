function populateCatalogue(obj)
{
    const container = document.getElementById("catalogue");
    addEbookButton(container);

    for (const [key, val] of Object.entries(obj))
    {
        console.log(val);
        const a = document.createElement("a"); a.className = "ebookItem";
        const thumbnail = document.createElement("img"); thumbnail.className = "ebookThumbnail";
        const bar = document.createElement("span"); bar.className = "ebookBar";

        const title = document.createElement("p"); title.className = "ebookTitle";
        

        const button = document.createElement("button"); button.textContent = "remove"; button.style.backgroundColor = "red";
        button.type = "submit"; button.onclick = function() {event.stopPropagation(); }

        const form = document.createElement("form"); form.method = "POST";
        const methodInput = document.createElement("input"); methodInput.value = "DELETE"; 
        methodInput.type = "hidden"; methodInput.name = "_method";

        const titleInput = document.createElement("input"); titleInput.name = "title";
         titleInput.value = val["title"]; titleInput.type = "hidden";

        title.textContent = val["title"];
        a.href = "/media/ebooks/" + val["title"] + ".pdf";
        thumbnail.src = "/media/tmp/" + val["thumbnail"];

        form.appendChild(methodInput);
        form.appendChild(titleInput);
        form.appendChild(button);
        bar.appendChild(title);
        bar.appendChild(form);
        a.appendChild(thumbnail);
        a.appendChild(bar);   

        container.appendChild(a);
    }
}

function addEbookButton(container) {
    const form = document.createElement("form");
    form.method = "POST";
    form.enctype = "multipart/form-data";

    const methodInput = document.createElement("input"); methodInput.value = "POST"; methodInput.type = "hidden"; methodInput.name = "_method";
    
    form.appendChild(methodInput);

    const input = document.createElement("input");
    input.type = "file";
    input.name = "ebookFile";
    input.style.display = "none";

    const label = document.createElement("label");
    label.className = "ebookItem";
    
    const thumbnail = document.createElement("img");
    thumbnail.className = "ebookThumbnail";
    thumbnail.src = "/media/add_book.png";

    label.appendChild(thumbnail);
    label.appendChild(input);

    input.addEventListener("change", () => {
        if (input.files.length > 0) {
            form.submit();
        }
    });

    form.appendChild(label);
    container.appendChild(form);

    label.addEventListener("click", () => input.click());
}
