<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $passphrase = $input['passphrase'] ?? '';

    if ($passphrase === 'Th3_53cr3t_15_0uT_Th3r3') {
        echo json_encode(['dbPassword' => 'i_4m_th3_d33b33']);
    } else {
        http_response_code(401);
        echo json_encode(['error' => 'Invalid passphrase']);
    }
} else {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
}
?>
