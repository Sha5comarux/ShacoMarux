<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $u = $_POST["username"] ?? "";
    $e = $_POST["email"] ?? "";
    $p = $_POST["password"] ?? "";

    if (($u === "admin" && $p === "dragon") || ($e === "prof@univ.dz" && $p === "123456")) {
        echo "<h1>SUCCES : Authentification validee !</h1>";
        exit;
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Portail Examen Prof</title></head>
<body>
    <h2>Connexion Serveur Examen</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username">
        <input type="text" name="email" placeholder="Email">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Connexion</button>
    </form>
</body>
</html>
