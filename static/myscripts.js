function divSelect(){
        
    var select = document.getElementById('expense_item');
    var expense_category = document.getElementById('expense_category').value;
    var x = Array("");
    var food = Array("Groceries", "Dining out");
    var rent = Array("House Rent", "Mortgage", "School Fees");
    var utilities = Array("Water", "Electricity", "Internet", "DTH connection");
    var insurance = Array("Health Insurance", "Vehicle Insurance", "Life Insurance");
    var loan = Array("Credit Card Payment", "Personal Loan", "Car Loan", "Installment");
    var transportation = Array("Vehicle's Fuel", "Vehicle's Maintenance", "Public transit");
    var entertainment = Array("Vacation", "Watching Movies", "Arcade");
    var memberships = Array("Gym", "Club", "OTT Platforms");
    
    select.options.length = 1;
    
        if(expense_category === ""){
            for(var i = 0; i< x.length; ++i) {
                select[select.length] = new Option(x[i], x[i]);
            }
        } else if(expense_category === "Food"){
            for(var i = 0; i< food.length; ++i) {
                select[select.length] = new Option(food[i], food[i]);
            }
        } else if(expense_category === "Rent"){
            for(var i = 0; i< rent.length; ++i) {
                select[select.length] = new Option(rent[i], rent[i]);
            }
        } else if(expense_category === "Utilities"){
            for(var i = 0; i< utilities.length; ++i) {
                select[select.length] = new Option(utilities[i], utilities[i]);
            }
        } else if(expense_category === "Insurance"){
            for(var i = 0; i< insurance.length; ++i) {
                select[select.length] = new Option(insurance[i], insurance[i]);
            }
        } else if(expense_category === "Loan"){
            for(var i = 0; i< loan.length; ++i) {
                select[select.length] = new Option(loan[i], loan[i]);
            }
        } else if(expense_category === "Transportation"){
            for(var i = 0; i< transportation.length; ++i) {
                select[select.length] = new Option(transportation[i], transportation[i]);
            }
        } else if(expense_category === "Entertainment"){
            for(var i = 0; i< entertainment.length; ++i) {
                select[select.length] = new Option(entertainment[i], entertainment[i]);
            }
        } else if(expense_category === "Memberships"){
            for(var i = 0; i< memberships.length; ++i) {
                select[select.length] = new Option(memberships[i], memberships[i]);
            }
        }
}