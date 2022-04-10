"use strict"
const inp_title = document.getElementById("inp-title");
const search_form = document.getElementById("search-form");
const badge_ingredients_add = document.getElementById("badge-ingredients-add");
const badge_ingredients_remove = document.getElementById("badge-ingredients-remove");
const badge_categories = document.getElementById("badge-categories");

const categories = getById("inp-category-");
const ingredientsAdd = getById("inp-add-");
const ingredientsRemove = getById("inp-remove-");
setIngredientsBadge();
setCategoriesBadge();

ingredientsAdd.forEach(inp =>
{
    const id = getId(inp.id, "inp-add-");
    let inpR;
    for (let i = 0; i < ingredientsRemove.length; i++)
    {
        const inp2 = ingredientsRemove[i];
        const id2 = getId(inp2.id, "inp-remove-");
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
    };
    categories.forEach(inp =>
    {
        if (inp.checked) data.categories.push(getId(inp.id, "inp-category-"));
    });
    ingredientsAdd.forEach(inp =>
    {
        if (inp.checked) data.ingredientsAdd.push(getId(inp.id, "inp-add-"));
    });
    ingredientsRemove.forEach(inp =>
    {
        if (inp.checked) data.ingredientsRemove.push(getId(inp.id, "inp-remove-"));
    });
    const dataFull = {};
    if (data.categories.length != 0) dataFull.categories = data.categories.join("-");
    if (data.ingredientsAdd.length != 0) dataFull.ingredientsAdd = data.ingredientsAdd.join("-");
    if (data.ingredientsRemove.length != 0) dataFull.ingredientsRemove = data.ingredientsRemove.join("-");
    const title = inp_title.value.trim();
    if (title != "") dataFull.title = title;
    const params = new URLSearchParams(dataFull).toString();
    window.location.href = "/?" + params
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
