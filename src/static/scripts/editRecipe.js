// editor.codemirror.getValue()

setInput("inp-category", "category-suggestions")
setInput("inp-ingredient", "ingredient-suggestions")


function setInput(inpId, listId)
{
    const inp_ingredient = document.getElementById(inpId);
    const inp_ingredient_list = document.getElementById(listId);

    inp_ingredient.addEventListener("change", () =>
    {
        for (let i = 0; i < inp_ingredient_list.firstElementChild.children.length; i++)
        {
            const option = inp_ingredient_list.firstElementChild.children[i];
            if (inp_ingredient.value == option.innerText) return;
        }
        inp_ingredient.value = "";
    });
}