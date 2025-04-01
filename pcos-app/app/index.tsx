import * as React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import SymptomUploadScreen from './SymptomUploadScreen';
import BloodUploadScreen from './BloodUploadScreen'
import HomeScreen from './HomeScreen';

const Stack = createNativeStackNavigator();

export default function Index() {
  
  return (
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
        />
        <Stack.Screen
          name="SymptomUpload"
          component={SymptomUploadScreen}
        />
        <Stack.Screen
          name="BloodUpload"
          component={BloodUploadScreen}
        />
      </Stack.Navigator>
  );
}
