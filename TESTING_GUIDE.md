# ExpenseSense Testing Guide

Complete guide to test all features of the ExpenseSense application.

## Prerequisites

### 1. Start the Backend Server
```bash
cd backend
python manage.py runserver
```
✅ Backend should be running on `http://localhost:8000`

### 2. Start the Flutter App
```bash
cd frontend
flutter run
```

Choose one of:
- **Chrome** (Web - easiest for testing)
- **iOS Simulator** (Open in Xcode: `open -a Xcode ios/Runner.xcworkspace`)
- **Android Emulator**

---

## Test Plan

### Phase 1: Authentication Flow

#### Test 1.1: Register New User
1. App opens → Splash screen (2 seconds)
2. No stored credentials → Redirects to **Login Screen**
3. Tap **"Don't have an account? Register"**
4. **Register Screen** appears
5. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
6. Tap **"Register"**
7. ✅ Success message appears
8. ✅ Redirects to **Dashboard**

**Expected Results**:
- ✅ Form validation works
- ✅ Password mismatch shows error
- ✅ Invalid email shows error
- ✅ Successful registration saves user
- ✅ Auto-login after registration

#### Test 1.2: Logout
1. From **Dashboard**, tap **Profile** icon (top right) OR bottom nav
2. Scroll to bottom
3. Tap **"Logout"** button (red)
4. Confirmation dialog appears
5. Tap **"Logout"**
6. ✅ Redirects to **Login Screen**

#### Test 1.3: Login with Credentials
1. On **Login Screen**, enter:
   - Email: `test@example.com`
   - Password: `password123`
2. Tap **"Login"**
3. ✅ Success message
4. ✅ Redirects to **Dashboard**

---

### Phase 2: Dashboard Features

#### Test 2.1: View Monthly Summary
1. On **Dashboard Screen**
2. ✅ Welcome message shows: "Welcome, testuser!"
3. ✅ Monthly summary card displays:
   - Current month and year
   - Total spent amount (₹0.00 initially)
   - Number of transactions (0 initially)
4. ✅ Category breakdown section (empty initially)

#### Test 2.2: Pull to Refresh
1. Pull down on dashboard
2. ✅ Refresh indicator appears
3. ✅ Data reloads
4. ✅ Loading indicator during refresh

---

### Phase 3: Add Expense (Manual Entry)

#### Test 3.1: Add First Expense
1. From **Dashboard**, tap **+ FAB** (floating action button)
2. **Add Expense Screen** appears
3. Fill in the form:
   - Amount: `250.50`
   - Merchant: `McDonald's`
   - Category: Select **"Food & Dining"**
   - Payment Mode: Select **"UPI"**
   - Date: Keep today's date (or select different)
   - Notes: `Lunch with team`
4. Tap **Save** icon (top right)
5. ✅ Success message: "Expense added successfully"
6. ✅ Navigates back to **Dashboard**
7. ✅ Dashboard now shows:
   - Total spent: ₹250.50
   - Transactions: 1
   - Category: Food & Dining - ₹250.50 (1 transaction)

**Expected Results**:
- ✅ All fields work correctly
- ✅ Category dropdown shows all 10 categories
- ✅ Payment mode dropdown shows all options
- ✅ Date picker works
- ✅ Form validation prevents empty amount/merchant
- ✅ Dashboard updates immediately

#### Test 3.2: Add More Expenses
Add these expenses to test different categories:

| Amount | Merchant | Category | Payment Mode |
|--------|----------|----------|--------------|
| ₹150 | Uber | Transport | UPI |
| ₹1200 | Amazon | Shopping | Card |
| ₹500 | PVR Cinemas | Entertainment | Card |
| ₹2500 | Electricity Bill | Bills | Net Banking |
| ₹800 | Apollo Pharmacy | Healthcare | Cash |

After adding all:
- ✅ Dashboard shows total: ₹5400.50
- ✅ Dashboard shows 6 transactions
- ✅ Category breakdown lists all 6 categories

---

### Phase 4: ML Classification Feature 🤖

#### Test 4.1: Classify SMS Text
1. Tap **+ FAB** to add expense
2. Scroll down to **"AI Classification (Optional)"** section
3. In SMS Text field, paste this:
   ```
   Spent Rs 450 at Starbucks using HDFC Credit Card on 15/01/2025
   ```
4. Tap the **AI icon** (⚡) button
5. ✅ Loading indicator appears
6. ✅ Category automatically selected: **"Food & Dining"**
7. ✅ Green snackbar shows: "Classified as: Food & Dining (XX.X% confidence)"
8. Fill in:
   - Amount: `450`
   - Merchant: `Starbucks`
9. Tap **Save**

**Test Different SMS Patterns**:

| SMS Text | Expected Category |
|----------|-------------------|
| "Paid Rs 80 for Ola ride" | Transport |
| "Purchased shoes for Rs 2500" | Shopping |
| "Netflix subscription Rs 499" | Entertainment |
| "Water bill Rs 350 paid" | Bills |
| "Doctor consultation Rs 800" | Healthcare |
| "Bought groceries for Rs 1200" | Groceries |
| "Flight ticket to Mumbai Rs 3500" | Travel |

✅ Each should automatically select the correct category

---

### Phase 5: Expense List Features

#### Test 5.1: View All Expenses
1. Tap **"Expenses"** in bottom navigation (or from dashboard)
2. **Expense List Screen** appears
3. ✅ All expenses displayed as cards
4. Each card shows:
   - ✅ Category icon with color
   - ✅ Merchant name (bold)
   - ✅ Category label
   - ✅ Date (formatted)
   - ✅ Amount (right side, bold)
   - ✅ Payment mode icon + label

#### Test 5.2: Filter by Category
1. Tap **Filter** icon (top right)
2. Filter dialog appears
3. Tap **"Food & Dining"** chip
4. Tap **"Apply"**
5. ✅ Only food expenses shown
6. ✅ Filter icon shows active state
7. Tap **Clear** icon (X) in app bar
8. ✅ All expenses visible again

#### Test 5.3: Filter by Date Range
1. Tap **Filter** icon
2. Tap **"Select"** next to Date Range
3. Date range picker appears
4. Select: Start = 1 week ago, End = Today
5. Tap **"Apply"** in dialog
6. ✅ Only expenses in range shown
7. Tap **"Clear"** in filter dialog
8. ✅ All expenses visible

#### Test 5.4: Combined Filters
1. Tap **Filter** icon
2. Select category: **"Transport"**
3. Select date range: Last 7 days
4. Tap **"Apply"**
5. ✅ Only transport expenses from last week shown

#### Test 5.5: View Expense Details
1. Tap on any **expense card**
2. ✅ Bottom sheet slides up
3. Details shown:
   - Amount with ₹ symbol
   - Merchant name
   - Category with icon
   - Payment mode with icon
   - Full date (formatted)
   - Notes (if added)
   - SMS text (if classified from SMS)
4. ✅ Delete button visible (red)
5. Tap **Close** icon (X)

#### Test 5.6: Swipe to Delete
1. Swipe any expense card **left**
2. ✅ Red background with delete icon appears
3. ✅ Confirmation dialog: "Are you sure?"
4. Tap **"Cancel"**
   - ✅ Card returns to normal
5. Swipe again, tap **"Delete"**
   - ✅ Green snackbar: "Expense deleted successfully"
   - ✅ Card disappears
   - ✅ Dashboard totals update

#### Test 5.7: Pull to Refresh
1. Pull down on expense list
2. ✅ Refresh indicator
3. ✅ Data reloads

#### Test 5.8: Empty State
1. Delete all expenses
2. ✅ Empty state shows:
   - Receipt icon (gray)
   - "No expenses yet"
   - "Tap the + button to add your first expense"

---

### Phase 6: Profile Screen Features

#### Test 6.1: View Profile Information
1. Tap **"Profile"** in bottom navigation
2. **Profile Screen** appears
3. ✅ Profile header with gradient:
   - Avatar circle
   - Username
   - Email
4. ✅ Account Information card:
   - Username with icon
   - Email with icon
   - Member since date
5. ✅ Statistics card:
   - Total expense count
   - Monthly expense count
   - Monthly total amount

#### Test 6.2: View Settings
1. Scroll to Settings section
2. ✅ Three options visible:
   - Notifications toggle
   - Change Password
   - About

#### Test 6.3: About Dialog
1. Tap **"About"**
2. ✅ About dialog appears:
   - App name: ExpenseSense
   - Version: 1.0.0
   - Icon
   - Description

#### Test 6.4: Placeholders
1. Tap **"Notifications"** toggle
   - ✅ Snackbar: "Coming soon!"
2. Tap **"Change Password"**
   - ✅ Snackbar: "Coming soon!"

---

### Phase 7: Navigation Flow

#### Test 7.1: Bottom Navigation
1. From **Dashboard** (tab 0)
   - Tap **Expenses** tab → Goes to Expense List
   - Tap **Profile** tab → Goes to Profile
   - Tap **Dashboard** tab → Returns to Dashboard
2. From **Expense List** (tab 1)
   - ✅ Bottom nav shows middle item selected
3. From **Profile** (tab 2)
   - ✅ Bottom nav shows right item selected

#### Test 7.2: Back Navigation
1. From Dashboard → Expense List
   - Tap **Back** → Returns to Dashboard
2. From Dashboard → Profile → Back
   - Returns to Dashboard
3. From Add Expense → Back
   - Returns to previous screen

---

## Advanced Testing

### Edge Cases

#### Test A1: Form Validation
1. Try to add expense with:
   - Empty amount → ✅ "Amount is required"
   - Zero amount → ✅ "Enter a valid amount"
   - Negative amount → ✅ Validation error
   - Empty merchant → ✅ "Merchant is required"
   - Very long merchant name (1000 chars) → ✅ Accepts but truncates in UI

#### Test A2: Network Errors
1. Stop the backend server
2. Try to add expense
   - ✅ Error snackbar: Connection refused
3. Try to load expenses
   - ✅ Error state
4. Start server again
5. Pull to refresh
   - ✅ Data loads successfully

#### Test A3: Large Dataset
1. Add 50+ expenses
2. Scroll through list
   - ✅ Smooth scrolling
   - ✅ No lag
3. Apply filters
   - ✅ Fast filtering

#### Test A4: Special Characters
1. Add expense with merchant: `Test & Co. (New)`
   - ✅ Saves correctly
   - ✅ Displays correctly
2. SMS classification with emojis:
   ```
   💰 Paid ₹500 at Café ☕
   ```
   - ✅ Should still classify

---

## Performance Testing

### Load Times
- ✅ Splash → Dashboard: < 2 seconds
- ✅ API calls: < 1 second
- ✅ ML classification: < 3 seconds
- ✅ List rendering: Instant
- ✅ Navigation: Instant

### Memory Usage
- Monitor during extended use
- Check for memory leaks
- Verify provider cleanup

---

## Platform-Specific Testing

### Web (Chrome)
- ✅ All features work
- ✅ Date pickers work
- ✅ Responsive design

### iOS
- ✅ Native UI components
- ✅ Swipe gestures smooth
- ✅ Safe area respected

### Android
- ✅ Material Design
- ✅ Back button behavior
- ✅ Permissions (if needed)

---

## Bug Reporting Template

If you find any issues, report using this format:

```
**Bug Title**: [Brief description]

**Screen**: [Login/Dashboard/etc]

**Steps to Reproduce**:
1. Step one
2. Step two
3. Step three

**Expected**: What should happen

**Actual**: What actually happened

**Platform**: [Web/iOS/Android]

**Error Message**: [If any]

**Screenshots**: [If applicable]
```

---

## Success Criteria

✅ All authentication flows work
✅ Manual expense entry works
✅ AI classification works
✅ Filters work correctly
✅ Delete functionality works
✅ Dashboard displays correct totals
✅ Navigation is smooth
✅ No crashes or freezes
✅ Error messages are user-friendly
✅ Loading states show properly

---

## Quick Test Checklist

Use this for rapid testing:

- [ ] Register new user
- [ ] Login
- [ ] Add 3 expenses manually
- [ ] Add 1 expense with SMS classification
- [ ] View expense list
- [ ] Filter by category
- [ ] Delete an expense
- [ ] Check dashboard totals
- [ ] View profile
- [ ] Logout
- [ ] Login again

---

## Next Steps After Testing

1. **If all tests pass**: ✅ Production ready!
2. **If issues found**: Document and fix
3. **Performance issues**: Profile and optimize
4. **UI improvements**: Based on user feedback

---

**Happy Testing! 🚀**
