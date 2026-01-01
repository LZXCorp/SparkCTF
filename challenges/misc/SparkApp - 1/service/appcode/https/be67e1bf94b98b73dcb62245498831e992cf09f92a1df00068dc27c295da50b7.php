<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode(['flag' => 'SPARK{3xp0rt3d_4cT1v1T135_4r3_fUn!!}']);
} else {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
}
?>