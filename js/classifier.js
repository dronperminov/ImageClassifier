function Classifier(labels) {
    this.labelsBlock = document.getElementById("labels")
    this.labels = []

    for (let i = 0; i < labels.length; i++) {
        this.labels.push({
            label: labels[i].label,
            html: labels[i].html == undefined ? labels[i].label : labels[i].html,
            color: labels[i].color,
            state: labels[i].checked != undefined,
            box: null,
        })
    }

    this.InitShortKeys()
    this.InitBoxes()
    this.InitStyles()

    let classifier = this
    document.addEventListener('keydown', function(e) { classifier.KeyDown(e) }) // обработка нажатия кнопок
}

// добавление элемента в список
Classifier.prototype.AddListItem = function(list, item) {
    let li = document.createElement("li")
    li.innerHTML = item
    list.appendChild(li)
}

// инициализация горячих клавиш
Classifier.prototype.InitShortKeys = function() {
    let keys = document.getElementById("keys")

    for (let i = 0; i < this.labels.length && i < 9; i++)
        this.AddListItem(keys, (i + 1) + " - " + this.labels[i].label)

    this.AddListItem(keys, "0 - reset")
    this.AddListItem(keys, "Enter - save")
}

// инициализация кнопок
Classifier.prototype.InitBoxes = function() {
    for (let i = 0; i < this.labels.length; i++) {
        this.labels[i].box = document.createElement("div")

        this.labels[i].box.className = "button checkbox"
        this.labels[i].box.innerHTML = this.labels[i].html

        let classifier = this

        this.labels[i].box.onclick = function() {
            if (!MULTICLASS)
                classifier.Reset()

            classifier.SetState(i, !classifier.labels[i].state);
        }

        this.labelsBlock.appendChild(this.labels[i].box)
        this.SetState(i, this.labels[i].state)
    }
}

Classifier.prototype.InitStyles = function() {
    let style = document.createElement('style');

    for (let i = 0; i < this.labels.length; i++) {
        let color = this.labels[i].color

        if (color == undefined || color == "")
            color = "#ffbc00"

        let css = ".checkbox-" + (i+1) + " { border-color: " + color + "; color: " + color + "}"
        css += " .checkbox-" + (i+1) + ":hover { border-color: " + color + "; color: " + color + "}"

        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
    }

    document.getElementsByTagName('head')[0].appendChild(style);
}

// установка значений заданной кнопке
Classifier.prototype.SetState = function(index, state) {
    this.labels[index].state = state

    if (state == false) {
        this.labels[index].box.classList.remove("checkbox-" + (index + 1))
    }
    else {
        this.labels[index].box.classList.remove("checkbox-" + (index + 1))
        this.labels[index].box.classList.add("checkbox-" + (index + 1))
    }
}

// сброс всех выбранных классов
Classifier.prototype.Reset = function() {
    for (let i = 0; i < this.labels.length; i++)
        this.SetState(i, false)
}

// сохранение разметки
Classifier.prototype.Save = function() {
    let result = []

    for (let i = 0; i < this.labels.length; i++)
        if (this.labels[i].state)
            result.push(this.labels[i].label)

    if (!REQUIRE_CONFIRMATION || confirm("Saving: are you sure?"))
        window.location.replace('/save?labels=' + result.join(";") + "&task_id=" + TASK_ID)
}

// обработка нажатия кнопок
Classifier.prototype.KeyDown = function(e) {
    if (e.key == "Enter") {
        this.Save()
        return
    }

    let index = parseInt(e.key)

    if (isNaN(index))
        return

    if (index == 0) {
        this.Reset()
    }
    else if (index <= this.labels.length) {
        if (!MULTICLASS)
            this.Reset()

        this.SetState(index - 1, !this.labels[index - 1].state)
    }

    e.preventDefault()
}