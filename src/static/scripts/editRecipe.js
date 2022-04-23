// editor.codemirror.getValue()
const urlSplited = window.location.href.split("/")
const recipeId = urlSplited[urlSplited.length - 1];
const btn_submit = document.getElementById("btn-submit");
const btn_delete = document.getElementById("btn-delete");
const btn_restore = document.getElementById("btn-restore");
const inp_title = document.getElementById("inp-title");
const img_container = document.getElementById("img-container");
const container_category = document.getElementById("container-category");
const container_ingredient = document.getElementById("container-ingredient");
const inp_img = document.getElementById("inp-img");
const openModal = setModal();
const modal_title = document.getElementById("modal-title");
const spinner = document.getElementById("spinner");
inp_title.focus();

const { setOptions: onDelete_category, options: options_category } = setInput("inp-category", "category-suggestions", "btn-category", getUsed_category, add_category);
const { setOptions: onDelete_ingredient, options: options_ingredient } = setInput("inp-ingredient", "ingredient-suggestions", "btn-ingredient", getUsed_ingredient, add_ingredient);


for (let i = 0; i < img_container.children.length; i++)
{
    const el = img_container.children[i];
    const btn = el.querySelector("button");
    btn.addEventListener("click", () => onImgDelete(el));
}
for (let i = 0; i < container_category.children.length; i++)
{
    const el = container_category.children[i];
    const btn = el.children[1];
    btn.addEventListener("click", () => delete_category(el));
}
for (let i = 0; i < container_ingredient.children.length; i += 2)
{
    const el1 = container_ingredient.children[i];
    const el2 = container_ingredient.children[i + 1];
    const btn = el2.children[1];
    btn.addEventListener("click", () => delete_ingredient(el1, el2));
}
inp_img.addEventListener("change", () =>
{
    if (inp_img.files.length > 0)
    {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(inp_img.files[0]);
        img.id = "-1"
        img.classList.add("img-fluid")
        const btn = document.createElement("button");
        btn.classList.add("btn");
        btn.classList.add("btn-danger");
        btn.classList.add("float-end");
        btn.innerText = "-";
        const div = document.createElement("div");
        const onload = () =>
        {
            img.removeEventListener("load", onload);
            const preview = createPreviewImg(img);
            formatImg(img);
            preview.style.position = "fixed";
            preview.style.left = "-3000px";
            preview.style.top = "-3000px";
            preview.style.width = "auto";
            preview.style.height = "auto";
            div.appendChild(preview);
            img_container.appendChild(div);
        }
        img.addEventListener("load", onload);
        div.appendChild(img);
        div.appendChild(btn);
        btn.addEventListener("click", () => onImgDelete(div));
    }
});

btn_submit.addEventListener("click", () =>
{
    btn_submit.disabled = true;
    btn_delete.disabled = true;
    spinner.classList.add("spinner-active");
    document.body.style.overflow = "hidden";

    const imgs = [];
    for (let i = 0; i < img_container.children.length; i++)
    {
        const img = img_container.children[i].firstElementChild;
        const preview = img_container.children[i].children[2];
        const id = `${parseInt(img.id, 10) > 0 ? img.id : -(i + 1)}`;
        imgs.push({
            id: id,
            img: img.src,
            preview: preview ? preview.src : null,
        });
    }

    const data = {
        title: inp_title.value,
        imgs: imgs,
        categories: getUsed_category().map(el => parseInt(el.id, 10)),
        ingredients: getUsed_ingredient().map(el => { return { id: parseInt(el.id, 10), count: el.count } }),
        description: editor.codemirror.getValue(),
    };
    fetch(`/api/editRecipe/${recipeId}`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
    }).then(async v =>
    {
        try
        {
            const json = await v.json();
            window.location.replace(`/recipe/${json.id || recipeId}`);
        }
        catch
        {
            window.location.replace(`/recipe/${recipeId}`);
        }
    }, r =>
    {
        if (`${recipeId}` == "0") window.location.replace(`/`);
        else window.location.replace(`/recipe/${recipeId}`);
    })
});
if (btn_delete)
{
    btn_delete.addEventListener("click", async () =>
    {
        modal_title.innerText = "Удалить рецепт?";
        if (await openModal())
        {
            btn_submit.disabled = true;
            btn_delete.disabled = true;
            spinner.classList.add("spinner-active");
            document.body.style.overflow = "hidden";

            fetch(`/api/deleteRecipe/${recipeId}`, {
                method: 'POST',
            }).finally(() =>
            {
                window.location.replace(`/`);
            })
        }
    })
}
if (btn_restore)
{
    btn_restore.addEventListener("click", async () =>
    {
        modal_title.innerText = "Восстановить рецепт?";
        if (await openModal())
        {
            btn_submit.disabled = true;
            btn_restore.disabled = true;
            spinner.classList.add("spinner-active");
            document.body.style.overflow = "hidden";

            fetch(`/api/restoreRecipe/${recipeId}`, {
                method: 'POST',
            }).finally(() =>
            {
                window.location.replace(`/recipe/${recipeId}`);
            })
        }
    })
}


function setInput(inpId, listId, btnId, getUsed, addNew)
{
    const inp_ingredient = document.getElementById(inpId);
    const inp_ingredient_list = document.getElementById(listId);
    const btn = document.getElementById(btnId);
    const options = []
    for (let i = 0; i < inp_ingredient_list.firstElementChild.children.length; i++)
    {
        const option = inp_ingredient_list.firstElementChild.children[i];
        options.push({ id: option.id, title: option.innerText });
    }

    inp_ingredient.addEventListener("change", () =>
    {
        for (let i = 0; i < options.length; i++)
        {
            const option = options[i];
            if (cs(inp_ingredient.value) == option.title) return;
        }
        inp_ingredient.value = "";
    });

    function setOptions()
    {
        const used = getUsed();
        inp_ingredient_list.firstElementChild.innerHTML = "";
        for (let i = 0; i < options.length; i++)
        {
            const data = options[i]
            let isUsed = false;
            for (let j = 0; j < used.length; j++)
            {
                const el = used[j];
                if (data.title == el)
                {
                    isUsed = true;
                    break
                }
            }
            if (isUsed) continue;
            const option = document.createElement("option");
            option.innerText = data.title;
            inp_ingredient_list.firstElementChild.appendChild(option);
        }
    }
    setOptions();
    btn.addEventListener("click", () =>
    {
        let exist = false;
        let opt = null
        for (let i = 0; i < options.length; i++)
        {
            const option = options[i];
            if (cs(inp_ingredient.value) == option.title)
            {
                exist = true;
                opt = option;
                break
            }
        }
        if (!exist) return;
        addNew(opt.id, opt.title);
        inp_ingredient.value = "";
        setOptions();
    });
    return { setOptions, options };
}

async function onImgDelete(el)
{
    modal_title.innerText = "Удалить картинку?";
    if (await openModal())
    {
        img_container.removeChild(el);
    }
}
function delete_category(el)
{
    container_category.removeChild(el);
    onDelete_category();
}
function delete_ingredient(el1, el2)
{
    container_ingredient.removeChild(el1);
    container_ingredient.removeChild(el2);
    onDelete_ingredient();
}

function setModal()
{
    let resolve_ = null;
    const modalEl = document.getElementById('modal')
    const modal = new bootstrap.Modal(modalEl);
    const btn_modal_ok = document.getElementById("btn-modal-ok");

    function openModal()
    {
        return new Promise((resolve, reject) =>
        {
            resolve_ = resolve;
            modal.show()
        });
    }

    modalEl.addEventListener('hidden.bs.modal', e =>
    {
        if (resolve_)
        {
            resolve_(false);
            resolve_ = null;
        }
    });
    btn_modal_ok.addEventListener("click", () =>
    {
        if (resolve_)
        {
            resolve_(true);
            resolve_ = null;
            modal.hide()
        }
    });
    return openModal;
}

function formatImg(img)
{
    img.src = scaleImg(img, 1280);
}
function createPreviewImg(img)
{
    const preview = document.createElement("img");
    preview.src = scaleImg(img, 200, true);
    return preview;
}
function scaleImg(img, MAXSize, useMin=false)
{
    const canvas = document.createElement("canvas");
    let width = img.width
    let height = img.height
    let maxSize = Math.max(width, height);
    if (useMin) maxSize = Math.min(width, height);
    if (maxSize > MAXSize)
    {
        const c = MAXSize / maxSize;
        width *= c;
        height *= c;
    }
    width = Math.round(width);
    height = Math.round(height);
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, width, height);
    return canvas.toDataURL();
}

function getUsed_category()
{
    const used = []
    for (let i = 0; i < container_category.children.length; i++)
    {
        const el = container_category.children[i];
        const text = el.firstElementChild;
        used.push({ title: cs(text.innerText), id: el.id });
    }
    return used;
}
function getUsed_ingredient()
{
    const used = []
    for (let i = 0; i < container_ingredient.children.length; i += 2)
    {
        const el1 = container_ingredient.children[i];
        const el2 = container_ingredient.children[i + 1];
        used.push({ title: cs(el1.innerText), id: el1.id, count: el2.firstElementChild.value });
    }
    // console.log(used);
    return used;
}
function add_category(id, title)
{
    const container = document.createElement("span");
    container.classList.add("badge");
    container.classList.add("bg-secondary");
    container.classList.add("fs-6");
    container.classList.add("me-2");
    container.id = id;
    const text = document.createElement("span");
    container.appendChild(text);
    text.innerText = title + " ";
    const btn = document.createElement("button");
    container.appendChild(btn);
    btn.innerText = "-";
    btn.classList.add("btn");
    btn.classList.add("btn-danger");

    btn.addEventListener("click", () => delete_category(container));
    container_category.appendChild(container);
}
function add_ingredient(id, title)
{
    const dt = document.createElement("dt");
    dt.classList.add("col-sm-3");
    dt.innerText = title;
    dt.id = id;
    const dd = document.createElement("dd");
    dd.classList.add("col-sm-9");
    const inp = document.createElement("input");
    dd.appendChild(inp);
    inp.classList.add("w-75");
    inp.type = "text";
    const btn = document.createElement("button");
    dd.appendChild(btn);
    btn.classList.add("btn");
    btn.classList.add("btn-danger");
    btn.classList.add("float-end");
    btn.innerText = "-";
    btn.addEventListener("click", () => delete_ingredient(dt, dd));
    container_ingredient.appendChild(dt);
    container_ingredient.appendChild(dd);
}

function cs(str)
{
    return str.replace(/\s+/g, " ").trim()
}



const editModal = document.getElementById("modal-edit");
const editModal_title = document.getElementById("modal-edit-title");
const editModal_table = document.getElementById("modal-edit-table");
const editModal_inp = document.getElementById("inp-modal-edit");
const editModal_btn = document.getElementById("btn-modal-edit");
const editModal_ok = document.getElementById("btn-modal-edit-ok");

const btn_addCategory = document.getElementById("btn-category-new");
const btn_addIngredient = document.getElementById("btn-ingredient-new");

const openModalAsync = createAsyncModal();

btn_addCategory.addEventListener("click", () => openAdder("category"))
btn_addIngredient.addEventListener("click", () => openAdder("ingredient"))

let editModal_curItems = [];
let editModal_newItems = [];

editModal_btn.addEventListener("click", () =>
{
    const value = editModal_inp.value.replace(/\s+/g, " ").trim();
    if (value != "" && !containsStr(editModal_curItems, value))
    {
        editModal_newItems.push(value);
        const li = document.createElement("li");
        editModal_table.appendChild(li);
        li.innerText = value;
    }
    editModal_inp.value = "";
});


async function openAdder(type)
{
    editModal_title.innerText = type == "category" ? "Категории" : "Ингредиенты";
    btn_addCategory.disabled = true;
    btn_addIngredient.disabled = true;
    document.body.style.overflow = "hidden";
    spinner.classList.add("spinner-active");
    editModal_newItems = [];

    editModal_curItems = await getItems(type);
    spinner.classList.remove("spinner-active");
    editModal_table.innerHTML = "";
    for (let i = 0; i < editModal_curItems.length; i++)
    {
        const item = editModal_curItems[i];
        const li = document.createElement("li");
        editModal_table.appendChild(li);
        li.innerText = item.title;
    }

    const r = await openModalAsync();

    if (editModal_newItems.length != 0 && r)
    {
        spinner.classList.add("spinner-active");
        await sendItems(type, editModal_newItems);
        spinner.classList.remove("spinner-active");
    }
    btn_addCategory.disabled = false;
    btn_addIngredient.disabled = false;
    document.body.style.overflow = "auto";
}

function createAsyncModal()
{
    let resolve_ = null;
    const modal = new bootstrap.Modal(editModal);
    function openModal()
    {
        return new Promise((resolve, reject) =>
        {
            resolve_ = resolve;
            modal.show()
        });
    }

    editModal.addEventListener('hidden.bs.modal', e =>
    {
        if (resolve_)
        {
            resolve_(false);
            resolve_ = null;
        }
    });
    editModal_ok.addEventListener("click", () =>
    {
        if (resolve_)
        {
            resolve_(true);
            resolve_ = null;
            modal.hide()
        }
    });
    return openModal;
}

function getItems(type)
{
    return new Promise((resolve, reject) =>
    {
        const url = type == "category" ? "/api/categories" : "/api/ingredients";
        fetch(url, {
            method: 'GET'
        }).then(async v =>
        {
            const json = await v.json();
            resolve(json.error ? [] : json);
        }, r =>
        {
            resolve([]);
        })
    });
}

function containsStr(list, value)
{
    value = value.replace(/\s+/g, " ").trim().toLowerCase();
    for (let i = 0; i < list.length; i++)
    {
        const el = list[i].title.replace(/\s+/g, " ").trim().toLowerCase();
        if (el == value) return true;
    }
    return false;
}

function sendItems(type, items)
{
    return new Promise((resolve, reject) =>
    {
        if (items.length == 0)
        {
            resolve();
            return
        }
        let sended = 0;
        const all = items.length
        const url = type == "category" ? "/api/categories" : "/api/ingredients";
        items.forEach(item => {
            fetch(url, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"title": item}),
            }).then(async v =>
            {
                const json = await v.json();
                if (json.id)
                {
                    if (type == "category")
                    {
                        options_category.push({ id: json.id, title: item });
                        onDelete_category();

                    }
                    else
                    {
                        options_ingredient.push({ id: json.id, title: item });
                        onDelete_ingredient();
                    }
                }
            }, () => { },
            ).finally(() =>
            {
                sended += 1;
                if (sended >= all)
                {
                    resolve()
                }
            })
        });
    });
}
