% rebase('templates/base.tpl', title=list_name)
<h2 class="list-heading"><a class="homebutton" href="/">&#8962;</a> | <a href="/l/{{list_name}}">{{list_name}}</a></h2>

<table class="table">
    % for index, item in enumerate(list_contents):
        <tr><td>
            <div class="row-inner">
             % if item['is_checked']:
                <strike>
             % end

            <a class="check-link" href="/l/{{list_name}}/check/{{index}}">
                {{item['text']}}
            </a>

             % if item['is_checked']:
                </strike>
             % end
            <a href="/l/{{list_name}}/delete/{{index}}">&times;</a>
            </div>
        </td></tr>
    % end
</table>

<form action="/l/{{list_name}}/update" method="POST">
    <input class="listadd col-xs-9 col-sm-9 col-md-9 col-lg-9" autofocus name="list_item_text" type="text"/>
    <input class="listsubmit col-xs-2 col-sm-2 col-md-2 col-lg-2" type="submit" value="add"/>
</form>
