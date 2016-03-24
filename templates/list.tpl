% rebase('templates/base.tpl', title=list_name)
<h2 class="list-heading"><a class="homebutton" href="/">&#8962;</a> | <a href="/l/{{list_name}}">{{list_name}}</a></h2>

<ul>
    % for index, item in enumerate(list_contents):
        <li>
            {{item}}
            <a href="/l/{{list_name}}/delete/{{index}}">&times;</a>
        </li>
    % end
</ul>

<form action="/l/{{list_name}}/update" method="POST">
    <input class="listadd" autofocus name="list_item" type="text"/>
    <input class="listsubmit" type="submit" value="add"/>
</form>
