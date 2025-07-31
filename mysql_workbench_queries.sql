-- =====================================================
-- Pet Adoption Platform - MySQL Workbench Queries
-- =====================================================
-- Copy and paste these queries into MySQL Workbench to view your data

-- 1. CONNECT TO YOUR DATABASE FIRST
-- Make sure you're connected to your pet adoption database
-- Database name should be something like 'pet_adoption_db' or similar

-- 2. VIEW ALL USERS AND THEIR PROFILES
SELECT 
    u.id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    u.is_active,
    u.date_joined,
    up.phone_number,
    up.address,
    up.city,
    up.state,
    up.zip_code,
    up.bio,
    up.is_shelter,
    up.shelter_name,
    up.shelter_description,
    up.created_at,
    up.updated_at
FROM auth_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
ORDER BY u.id;

-- 3. VIEW ONLY SHELTER USERS
SELECT 
    u.id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    up.shelter_name,
    up.shelter_description,
    up.phone_number,
    up.address,
    up.city,
    up.state,
    up.zip_code,
    u.date_joined
FROM auth_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE up.is_shelter = 1
ORDER BY u.id;

-- 4. VIEW ALL PETS
SELECT 
    p.id,
    p.name,
    p.pet_type,
    p.breed,
    p.age,
    p.gender,
    p.description,
    p.status,
    p.image,
    p.created_at,
    p.updated_at,
    u.username as owner_username,
    up.shelter_name as shelter_name
FROM pets_pet p
LEFT JOIN auth_user u ON p.owner_id = u.id
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
ORDER BY p.id;

-- 5. VIEW PETS BY STATUS
SELECT 
    p.name,
    p.pet_type,
    p.breed,
    p.age,
    p.status,
    u.username as owner
FROM pets_pet p
LEFT JOIN auth_user u ON p.owner_id = u.id
ORDER BY p.status, p.name;

-- 6. VIEW ALL ADOPTION REQUESTS
SELECT 
    ar.id,
    ar.reason,
    ar.status,
    ar.created_at,
    ar.updated_at,
    -- User requesting adoption
    u.username as requester_username,
    u.email as requester_email,
    u.first_name as requester_first_name,
    u.last_name as requester_last_name,
    -- Pet being adopted
    p.name as pet_name,
    p.pet_type as pet_type,
    p.breed as pet_breed,
    -- Shelter owner
    s.username as shelter_username,
    s.email as shelter_email,
    sp.shelter_name as shelter_name
FROM adoption_adoptionrequest ar
LEFT JOIN auth_user u ON ar.user_id = u.id
LEFT JOIN pets_pet p ON ar.pet_id = p.id
LEFT JOIN auth_user s ON p.owner_id = s.id
LEFT JOIN accounts_userprofile sp ON s.id = sp.user_id
ORDER BY ar.id;

-- 7. VIEW ADOPTION REQUESTS BY STATUS
SELECT 
    ar.status,
    COUNT(*) as count
FROM adoption_adoptionrequest ar
GROUP BY ar.status;

-- 8. VIEW ADOPTION REQUESTS FOR SHELTERS
SELECT 
    sp.shelter_name,
    p.name as pet_name,
    ar.status as request_status,
    requester.username as requester_username,
    requester.email as requester_email,
    ar.reason,
    ar.created_at
FROM adoption_adoptionrequest ar
LEFT JOIN pets_pet p ON ar.pet_id = p.id
LEFT JOIN auth_user shelter_user ON p.owner_id = shelter_user.id
LEFT JOIN accounts_userprofile sp ON shelter_user.id = sp.user_id
LEFT JOIN auth_user requester ON ar.user_id = requester.id
WHERE sp.is_shelter = 1
ORDER BY sp.shelter_name, ar.created_at DESC;

-- 9. VIEW ALL CHAT MESSAGES
SELECT 
    cm.id,
    cm.content,
    cm.created_at,
    cm.updated_at,
    -- Sender
    sender.username as sender_username,
    sender.email as sender_email,
    -- Receiver
    receiver.username as receiver_username,
    receiver.email as receiver_email
FROM chat_message cm
LEFT JOIN auth_user sender ON cm.sender_id = sender.id
LEFT JOIN auth_user receiver ON cm.receiver_id = receiver.id
ORDER BY cm.id;

-- 10. SUMMARY STATISTICS
SELECT 
    'Users' as category,
    COUNT(*) as total_count,
    COUNT(CASE WHEN up.is_shelter = 1 THEN 1 END) as shelter_count,
    COUNT(CASE WHEN up.is_shelter = 0 OR up.is_shelter IS NULL THEN 1 END) as regular_user_count
FROM auth_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id

UNION ALL

SELECT 
    'Pets' as category,
    COUNT(*) as total_count,
    COUNT(CASE WHEN p.status = 'available' THEN 1 END) as available_count,
    COUNT(CASE WHEN p.status = 'adopted' THEN 1 END) as adopted_count
FROM pets_pet p

UNION ALL

SELECT 
    'Adoption Requests' as category,
    COUNT(*) as total_count,
    COUNT(CASE WHEN ar.status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN ar.status = 'approved' THEN 1 END) as approved_count
FROM adoption_adoptionrequest ar

UNION ALL

SELECT 
    'Chat Messages' as category,
    COUNT(*) as total_count,
    NULL as shelter_count,
    NULL as regular_user_count
FROM chat_message;

-- 11. VIEW RECENT ACTIVITY
SELECT 
    'Recent Users' as activity_type,
    u.username,
    u.date_joined as activity_date,
    'User registered' as description
FROM auth_user u
ORDER BY u.date_joined DESC
LIMIT 10

UNION ALL

SELECT 
    'Recent Pets' as activity_type,
    p.name as username,
    p.created_at as activity_date,
    CONCAT('Pet added: ', p.pet_type, ' - ', p.breed) as description
FROM pets_pet p
ORDER BY p.created_at DESC
LIMIT 10

UNION ALL

SELECT 
    'Recent Adoption Requests' as activity_type,
    CONCAT(u.username, ' -> ', p.name) as username,
    ar.created_at as activity_date,
    CONCAT('Adoption request: ', ar.status) as description
FROM adoption_adoptionrequest ar
LEFT JOIN auth_user u ON ar.user_id = u.id
LEFT JOIN pets_pet p ON ar.pet_id = p.id
ORDER BY ar.created_at DESC
LIMIT 10;

-- 12. VIEW SHELTER-SPECIFIC DATA
SELECT 
    'Shelter Pets' as data_type,
    sp.shelter_name,
    p.name as pet_name,
    p.pet_type,
    p.status,
    p.created_at
FROM pets_pet p
LEFT JOIN auth_user u ON p.owner_id = u.id
LEFT JOIN accounts_userprofile sp ON u.id = sp.user_id
WHERE sp.is_shelter = 1
ORDER BY sp.shelter_name, p.created_at;

-- 13. VIEW ALL TABLES IN DATABASE
SHOW TABLES;

-- 14. VIEW TABLE STRUCTURES
DESCRIBE auth_user;
DESCRIBE accounts_userprofile;
DESCRIBE pets_pet;
DESCRIBE adoption_adoptionrequest;
DESCRIBE chat_message;

-- 15. COUNT RECORDS IN EACH TABLE
SELECT 'auth_user' as table_name, COUNT(*) as record_count FROM auth_user
UNION ALL
SELECT 'accounts_userprofile' as table_name, COUNT(*) as record_count FROM accounts_userprofile
UNION ALL
SELECT 'pets_pet' as table_name, COUNT(*) as record_count FROM pets_pet
UNION ALL
SELECT 'adoption_adoptionrequest' as table_name, COUNT(*) as record_count FROM adoption_adoptionrequest
UNION ALL
SELECT 'chat_message' as table_name, COUNT(*) as record_count FROM chat_message; 