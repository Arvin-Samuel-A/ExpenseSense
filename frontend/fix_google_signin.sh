#!/bin/bash

# Google Sign-In Fix - Rebuild Script
# Run this after modifying Info.plist

echo "🔧 Fixing Google Sign-In Configuration..."
echo ""

cd "$(dirname "$0")"

echo "1️⃣ Cleaning Flutter build..."
flutter clean

echo ""
echo "2️⃣ Getting dependencies..."
flutter pub get

echo ""
echo "3️⃣ Cleaning iOS build..."
cd ios
rm -rf Pods
rm -f Podfile.lock
echo "Installing pods..."
pod install

cd ..

echo ""
echo "✅ Build cleaned and dependencies installed!"
echo ""
echo "📱 Next steps:"
echo "1. Close Xcode if it's open"
echo "2. Run: open ios/Runner.xcworkspace"
echo "3. In Xcode: Product → Clean Build Folder (Cmd+Shift+K)"
echo "4. In Xcode: Product → Run (Cmd+R)"
echo "5. Test Google Sign-In!"
echo ""
