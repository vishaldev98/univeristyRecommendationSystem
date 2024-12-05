<?php
session_start(); // Start the session for managing user interactions with the chatbot

// Function to handle the chatbot interaction
function handleTicketBotInteraction($message) {
    $reply = '';

    // Initialize session step if not set
    if (!isset($_SESSION['step'])) {
        $_SESSION['step'] = 0; // Set to 0 to start the conversation
    }

    switch ($_SESSION['step']) {
        case 0:
            $reply = "Hi! What is your name?";
            $_SESSION['step'] = 1;
            break;
        case 1:
            if (!empty($message)) {
                $_SESSION['name'] = $message;
                $reply = "Hi " . $_SESSION['name'] . "! What category does your issue fall under? (e.g., Billing, Technical, General)";
                $_SESSION['step'] = 2;
            }
            break;
        case 2:
            if (!empty($message)) {
                // Normalize and check if the category is valid
                $message = strtolower(trim($message));

                if (in_array($message, ['billing', 'technical', 'general'])) {
                    $_SESSION['category'] = ucfirst($message);  // Capitalize the category for consistency
                    $reply = "Got it. Can you briefly describe the issue?";
                    $_SESSION['step'] = 3;
                } else {
                    $reply = "Please provide a valid category (Billing, Technical, or General).";  // Invalid category message
                }
            }
            break;
        case 3:
            if (!empty($message)) {
                $_SESSION['description'] = $message;
                $reply = "What priority is this issue? (Low, Medium, High)";
                $_SESSION['step'] = 4;
            }
            break;
        case 4:
            if (!empty($message)) {
                // Normalize and check if the priority is valid
                $message = strtolower(trim($message));

                if (in_array($message, ['low', 'medium', 'high'])) {
                    $_SESSION['priority'] = ucfirst($message);  // Capitalize the priority for consistency
                    $ticketId = uniqid("TICKET_");
                    $ticketData = [
                        'ticket_id' => $ticketId,
                        'name' => $_SESSION['name'],
                        'category' => $_SESSION['category'],
                        'description' => $_SESSION['description'],
                        'priority' => $_SESSION['priority'],
                    ];
                    file_put_contents('tickets.json', json_encode($ticketData) . PHP_EOL, FILE_APPEND);
                    $reply = "Thank you! Your ticket has been created with ID: $ticketId. Our team will get back to you shortly.";
                    $_SESSION['step'] = 5; // Proceed to final step
                } else {
                    $reply = "Please provide a valid priority (Low, Medium, High).";  // Invalid priority message
                }
            }
            break;
        case 5:
            $reply = "Thank you for contacting us! The chat will now close.";
            session_destroy(); // Clear session after ticket creation and end the conversation
            break;
        default:
            $reply = "Something went wrong. Please refresh the page.";
            session_destroy(); // Reset if something fails
            break;
    }

    return ['reply' => $reply]; // Return the reply message
}

// Handle user interaction and ticket creation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $message = $_POST['message'] ?? '';  // Get the message from POST data
    $response = handleTicketBotInteraction($message); // Handle the interaction
    echo json_encode($response); // Return the response
    exit;
}
?>
