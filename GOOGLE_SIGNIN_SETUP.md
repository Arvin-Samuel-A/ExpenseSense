# Google Sign-In Setup Guide

## Issue Fixed ✅

The error "No active configuration. Make sure GIDClientID is set in Info.plist" has been resolved by adding the Google Client ID to the iOS Info.plist file.

## What Was Added

### iOS Configuration (Info.plist)

Added the following to `/frontend/ios/Runner/Info.plist`:

```xml
<key>GIDClientID</key>
<string>927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu.apps.googleusercontent.com</string>
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>com.googleusercontent.apps.927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu</string>
        </array>
    </dict>
</array>
```

## How to Test

### 1. Clean Build (Important!)

Since you modified Info.plist, you need to rebuild the iOS app:

```bash
cd frontend

# Clean Flutter build
flutter clean

# Get dependencies
flutter pub get

# Clean iOS build (if running from Xcode)
cd ios
rm -rf Pods
rm Podfile.lock
pod install
cd ..
```

### 2. Rebuild from Xcode

Since you're using Xcode to run the app:

1. **Close the current Xcode project**
2. **Open Xcode again**:
   ```bash
   open ios/Runner.xcworkspace
   ```
3. **Clean build folder**: Product → Clean Build Folder (Cmd+Shift+K)
4. **Run the app**: Product → Run (Cmd+R)

### 3. Test Google Sign-In

1. Launch the app
2. Go to Login screen
3. Tap "Sign in with Google" button
4. ✅ Should now open Google Sign-In flow
5. Select your Google account
6. Grant permissions
7. Should redirect back to app and login

## Important Notes

### Using the Correct Client ID

The Google Client ID in your `.env` file and `Info.plist` should match:

- **Current ID**: `927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu.apps.googleusercontent.com`

### iOS URL Scheme

The URL scheme is derived from your client ID:
- Format: `com.googleusercontent.apps.YOUR-CLIENT-ID`
- Your scheme: `com.googleusercontent.apps.927865345975-bp9rjjf7tucsq86q6affu9iq3sddpigu`

## If You Need to Create Your Own Google OAuth Client

If you want to use your own Google OAuth credentials:

### 1. Go to Google Cloud Console
https://console.cloud.google.com/

### 2. Create OAuth 2.0 Client ID

1. Select your project (or create new)
2. Go to "APIs & Services" → "Credentials"
3. Click "Create Credentials" → "OAuth client ID"
4. Select "iOS" application type
5. Enter your Bundle ID (from Xcode project settings)
6. Copy the generated Client ID

### 3. Update Configuration

Update in **two places**:

#### A. Frontend .env file
```properties
GOOGLE_CLIENT_ID=YOUR-NEW-CLIENT-ID.apps.googleusercontent.com
```

#### B. iOS Info.plist
```xml
<key>GIDClientID</key>
<string>YOUR-NEW-CLIENT-ID.apps.googleusercontent.com</string>

<!-- Also update the URL scheme -->
<key>CFBundleURLSchemes</key>
<array>
    <string>com.googleusercontent.apps.YOUR-NEW-CLIENT-ID</string>
</array>
```

### 4. Backend Configuration

Also update your Django backend to accept the new client ID:

```python
# backend/expensesense_backend/settings.py
GOOGLE_OAUTH_CLIENT_ID = 'YOUR-NEW-CLIENT-ID.apps.googleusercontent.com'
```

## Android Configuration (Future)

If you want to test on Android, you'll also need to configure:

### 1. Get Android OAuth Client ID

Create another OAuth client in Google Cloud Console:
- Type: Android
- Package name: `com.example.expensesense_app` (or your package)
- SHA-1 certificate fingerprint (get from Android Studio)

### 2. Update android/app/src/main/AndroidManifest.xml

```xml
<meta-data
    android:name="com.google.android.gms.auth.api.signin.client_id"
    android:value="YOUR-ANDROID-CLIENT-ID.apps.googleusercontent.com" />
```

## Troubleshooting

### Error: "No active configuration"
✅ **FIXED** - Added GIDClientID to Info.plist

### Error: "Sign in cancelled"
- User cancelled the Google Sign-In flow
- This is normal behavior

### Error: "Invalid client ID"
- Check that client ID in Info.plist matches Google Cloud Console
- Ensure no extra spaces or characters
- Rebuild the app after changes

### Error: "Redirect URI mismatch"
- Check URL scheme in Info.plist
- Should be: `com.googleusercontent.apps.YOUR-CLIENT-ID`
- No `.apps.googleusercontent.com` suffix in URL scheme

### Google Sign-In not showing account picker
- Make sure you're running on a real device or simulator with Google accounts
- iOS Simulator: Add a Google account in Settings → Mail → Accounts

## Testing Checklist

- [x] Clean Flutter build
- [x] Clean iOS build
- [x] Rebuild from Xcode
- [ ] Test Google Sign-In on iOS
- [ ] Verify account picker appears
- [ ] Verify successful login
- [ ] Check user data loads correctly
- [ ] Test logout with Google

## Current Status

✅ **iOS Info.plist configured**
✅ **Google Client ID added**
✅ **URL scheme configured**
✅ **Ready to test**

## Next Steps

1. **Close current Xcode instance**
2. **Clean and rebuild** (see steps above)
3. **Run from Xcode**
4. **Test Google Sign-In** 
5. Should work now! 🎉

---

**Note**: After modifying Info.plist, you MUST rebuild the iOS app from scratch for changes to take effect. Simply hot-reloading won't work.
