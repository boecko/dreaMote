//
//  EventListController.h
//  Untitled
//
//  Created by Moritz Venn on 09.03.08.
//  Copyright 2008 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface EventListController : UIViewController <UITableViewDelegate, UITableViewDataSource> {
@private
	NSArray *_events;
}

+ (EventListController*)withEventList: (NSArray*) eventList;
- (void)reloadData;

@property (nonatomic, retain) NSArray *events;

@end
