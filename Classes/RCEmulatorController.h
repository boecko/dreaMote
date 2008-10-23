//
//  RCEmulatorController.h
//  Untitled
//
//  Created by Moritz Venn on 23.07.08.
//  Copyright 2008 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface RCEmulatorController : UIViewController {
@private
	BOOL _shouldVibrate;
	UIView *rcView;
	UIView *screenView;
	UIImageView *imageView;
	UIToolbar *toolbar;
	UIButton *screenshotButton;

	NSInteger _screenshotType;
}

@end
