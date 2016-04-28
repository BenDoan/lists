% rebase('base.tpl', title=title)
<h2>Lists</h2>
<table class="table">
    % for list_name in lists:
        <tr>
            <td><div class="row-inner"><a href="/l/{{list_name}}">{{list_name}}</a></div></td>
        </tr>
    % end
</table>
<form action="/s/add" method="POST">
    <input class="listadd col-xs-9 col-sm-9 col-md-9 col-lg-9" autofocus name="list_name" type="text"/>
    <input class="listsubmit col-xs-2 col-sm-2 col-md-2 col-lg-2" type="submit" value="add"/>
</form>
