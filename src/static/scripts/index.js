"use strict"
const inp_title = document.getElementById("inp-title");
const search_form = document.getElementById("search-form");

const categories = getById("inp-category-");
const ingredientsAdd = getById("inp-add-");
const ingredientsRemove = getById("inp-remove-");


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
