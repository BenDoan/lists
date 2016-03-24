% rebase('templates/base.tpl', title=title)
<h2>Lists</h2>
<ul>
    % for list_name in lists:
        <li>
            <a href="/l/{{list_name}}">{{list_name}}</a>
        </li>
    % end
</ul>

<form action="/s/add" method="POST">
    <input class="listadd" autofocus name="list_name" type="text"/>
    <input class="listsubmit" type="submit" value="add"/>
</form>
