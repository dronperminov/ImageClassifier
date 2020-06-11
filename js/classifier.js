// инициализация кнопок и хоткеев
function Init() {
    let labels = document.getElementById("labels")
    let keys = document.getElementById("keys")
    let style = document.createElement('style');

    for (let i = 0; i < LABELS.length; i++) {
        let box = document.createElement("input")
        box.type = "checkbox"
        box.className = "checkbox checkbox-" + (i+1)
        box.setAttribute("data", LABELS[i].label)

        box.onclick = function() {
            if (!MULTICLASS) {
                Reset()
                this.checked = true;
            }
        }

        if (LABELS[i].checked != undefined) {
            if (!MULTICLASS)
                Reset()

            box.checked = true
        }

        labels.appendChild(box)
        labels.appendChild(document.createElement("br"))

        let li = document.createElement("li")
        li.innerHTML = (i + 1) + " - " + LABELS[i].label
        keys.appendChild(li)


        if (LABELS[i].color == undefined)
            continue

        let css = ".checkbox-" + (i+1) + ":checked:after {border-color: " + LABELS[i].color + "; color: " + LABELS[i].color + "}"
        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
    }

    let li = document.createElement("li")
    li.innerHTML = "Enter - save"
    keys.appendChild(li)

    document.getElementsByTagName('head')[0].appendChild(style);
}

// сброс всех выбранных классов
function Reset() {
    let labels = document.getElementsByClassName("checkbox")

    for (let i = 0; i < labels.length; i++)
        labels[i].checked = false
}

// обработка нажатия кнопок
document.addEventListener('keydown', function(e) {
    if (e.key == "Enter") {
        Save()
        return
    }

    let index = parseInt(e.key)
    let labels = document.getElementsByClassName("checkbox")
    
    if (isNaN(index))
        return

    if (index == 0) {
        Reset()
    }
    else if (index <= labels.length) {
        if (!MULTICLASS)
            Reset()

        labels[index - 1].checked = !labels[index - 1].checked
    }

    e.preventDefault()
})

function Save() {
    let labels = document.getElementsByClassName("checkbox")
    let result = []

    for (let i = 0; i < labels.length; i++)
        if (labels[i].checked)
            result.push(LABELS[i].label)

    if (!REQUIRE_CONFIRMATION || confirm("Saving: are you sure?"))
        window.location.replace('/save?labels=' + result.join(";") + "&task_id=" + TASK_ID)
}