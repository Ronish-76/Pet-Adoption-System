-- Pet Adoption Platform - View All Data
-- Run these queries in your MySQL Workbench to see all data

-- 1. View all users and their profiles
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

-- 2. View all pets
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

-- 3. View all adoption requests
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

-- 4. View all chat messages
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
FROM chat_chatmessage cm
LEFT JOIN auth_user sender ON cm.sender_id = sender.id
LEFT JOIN auth_user receiver ON cm.receiver_id = receiver.id
ORDER BY cm.id;

-- 5. Summary statistics
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
FROM chat_chatmessage;

-- 6. View recent activity (last 10 entries)
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

-- 7. View shelter-specific data
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

-- 8. View adoption requests by shelter
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