% rebase('templates/base.tpl', title=title)
<h2>Lists</h2>
<ul>
    % for list_name in lists:
        <li><a href="/l/{{list_name}}">{{list_name}}</a></li>
    % end
</ul>
