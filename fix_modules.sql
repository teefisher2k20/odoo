-- Update all modules to set to_buy = false
UPDATE ir_module_module SET to_buy = false WHERE to_buy = true;

-- Show how many modules were updated
SELECT COUNT(*) as updated_modules FROM ir_module_module WHERE to_buy = false;
