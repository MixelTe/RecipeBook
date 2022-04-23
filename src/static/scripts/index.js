"use strict"
const inp_title = document.getElementById("inp-title");
const search_form = document.getElementById("search-form");
const badge_ingredients_add = document.getElementById("badge-ingredients-add");
const badge_ingredients_remove = document.getElementById("badge-ingredients-remove");
const badge_users_add = document.getElementById("badge-users-add");
const badge_users_remove = document.getElementById("badge-users-remove");
const badge_categories = document.getElementById("badge-categories");

const categories = getById("inp-category-");
const ingredientsAdd = getById("inp-ingredient-add-");
const ingredientsRemove = getById("inp-ingredient-remove-");
const usersAdd = getById("inp-users-add-");
const usersRemove = getById("inp-users-remove-");
setIngredientsBadge();
setUsersBadge();
setCategoriesBadge();

ingredientsAdd.forEach(inp =>
{
    const id = getId(inp.id, "inp-ingredient-add-");
    let inpR;
    for (let i = 0; i < ingredientsRemove.length; i++)
    {
        const inp2 = ingredientsRemove[i];
        const id2 = getId(inp2.id, "inp-ingredient-remove-");
        if (id == id2)
        {
            inpR = inp2
            break;
        }
    }
    if (!inpR) return;
    inp.addEventListener("change", () =>
    {
        if (inp.checked) inpR.checked = false;
        setIngredientsBadge()
    });
    inpR.addEventListener("change", () =>
    {
        if (inpR.checked) inp.checked = false;
        setIngredientsBadge()
    });
});
usersAdd.forEach(inp =>
    {
        const id = getId(inp.id, "inp-users-add-");
        let inpR;
        for (let i = 0; i < usersRemove.length; i++)
        {
            const inp2 = usersRemove[i];
            const id2 = getId(inp2.id, "inp-users-remove-");
            if (id == id2)
            {
                inpR = inp2
                break;
            }
        }
        if (!inpR) return;
        inp.addEventListener("change", () =>
        {
            if (inp.checked) inpR.checked = false;
            setUsersBadge()
        });
        inpR.addEventListener("change", () =>
        {
            if (inpR.checked) inp.checked = false;
            setUsersBadge()
        });
    });
categories.forEach(inp =>
{
    inp.addEventListener("change", setCategoriesBadge);
})
function setIngredientsBadge()
{
    let countAdd = 0;
    let countRemove = 0;
    ingredientsAdd.forEach(inp => countAdd += inp.checked ? 1 : 0);
    ingredientsRemove.forEach(inp => countRemove += inp.checked ? 1 : 0);
    badge_ingredients_add.innerText = countAdd == 0 ? "" : `${countAdd}`;
    badge_ingredients_remove.innerText = countRemove == 0 ? "" : `-${countRemove}`;
}
function setUsersBadge()
{
    let countAdd = 0;
    let countRemove = 0;
    usersAdd.forEach(inp => countAdd += inp.checked ? 1 : 0);
    usersRemove.forEach(inp => countRemove += inp.checked ? 1 : 0);
    badge_users_add.innerText = countAdd == 0 ? "" : `${countAdd}`;
    badge_users_remove.innerText = countRemove == 0 ? "" : `-${countRemove}`;
}
function setCategoriesBadge()
{
    let count = 0;
    categories.forEach(inp => count += inp.checked ? 1 : 0);
    badge_categories.innerText = count == 0 ? "" : `${count}`;
}


function getById(id)
{
    return document.querySelectorAll(`[id^="${id}"]`);
}
function getId(id, prefix)
{
    return id.substring(prefix.length);
}

search_form.addEventListener("submit", e =>
{
    e.preventDefault();
    const data = {
        categories: [],
        ingredientsAdd: [],
        ingredientsRemove: [],
        usersAdd: [],
        usersRemove: [],
    };
    categories.forEach(inp =>
    {
        if (inp.checked) data.categories.push(getId(inp.id, "inp-category-"));
    });
    ingredientsAdd.forEach(inp =>
    {
        if (inp.checked) data.ingredientsAdd.push(getId(inp.id, "inp-ingredient-add-"));
    });
    ingredientsRemove.forEach(inp =>
    {
        if (inp.checked) data.ingredientsRemove.push(getId(inp.id, "inp-ingredient-remove-"));
    });
    usersAdd.forEach(inp =>
    {
        if (inp.checked) data.usersAdd.push(getId(inp.id, "inp-users-add-"));
    });
    usersRemove.forEach(inp =>
    {
        if (inp.checked) data.usersRemove.push(getId(inp.id, "inp-users-remove-"));
    });
    const dataFull = {};
    if (data.categories.length != 0) dataFull.categories = data.categories.join("-");
    if (data.ingredientsAdd.length != 0) dataFull.ingredientsAdd = data.ingredientsAdd.join("-");
    if (data.ingredientsRemove.length != 0) dataFull.ingredientsRemove = data.ingredientsRemove.join("-");
    if (data.usersAdd.length != 0) dataFull.usersAdd = data.usersAdd.join("-");
    if (data.usersRemove.length != 0) dataFull.usersRemove = data.usersRemove.join("-");
    const title = inp_title.value.trim();
    if (title != "") dataFull.title = title;
    const params = new URLSearchParams(dataFull);
    const curUrlParams = new URLSearchParams(window.location.search);
    if (curUrlParams.has("d")) params.append("d", "")
    window.location.href = "/?" + params.toString()
    return false;
});


const pageBtns = getById("btn-page-");
pageBtns.forEach(btn =>
{
    const id = getId(btn.id, "btn-page-");
    btn.addEventListener("click", () =>
    {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (id == "next" || id == "prev")
        {
            const page = urlParams.get("page") || 0;
            urlParams.set("page", parseInt(page, 10) + (id == "next" ? 1 : -1))
        }
        else
        {
            urlParams.set("page", parseInt(id, 10))
        }
        window.location.href = "/?" + urlParams.toString()
    });
});
