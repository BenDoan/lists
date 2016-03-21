% rebase('templates/base.tpl', title=list_name)
<h2>{{list_name}}</h2>

<ul>
    % for item in list_contents:
        <li>{{item}}</li>
    % end
</ul>
