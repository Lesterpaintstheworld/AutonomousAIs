<?php
$output = shell_exec('/var/www/html/synthetic-souls/venv/bin/python -m aider_nova --yes --cache-prompts --gui  2>&1');
echo "<pre>$output</pre>";
?>