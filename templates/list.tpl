% rebase('templates/base.tpl', title=list_name)
<h2><a class="homebutton" href="/">&#8962;</a> | {{list_name}}</h2>

<ul>
    % for index, item in enumerate(list_contents):
        <li>
            {{item}}
            <a href="/l/{{list_name}}/delete/{{index}}">&times;</a>
        </li>
    % end
</ul>

<form action="/l/{{list_name}}/update" method="POST">
    <input name="list_item" type="text"/>
    <input type="submit" value="add"/>
</form>
