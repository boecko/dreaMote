//
//  EventListController.m
//  Untitled
//
//  Created by Moritz Venn on 09.03.08.
//  Copyright 2008 __MyCompanyName__. All rights reserved.
//

#import "EventListController.h"

#import "EventTableViewCell.h"
#import "EventViewController.h"

#import "RemoteConnectorObject.h"
#import "FuzzyDateFormatter.h"

#import "Objects/Generic/Service.h"
#import "Objects/EventProtocol.h"

@implementation EventListController

@synthesize dateFormatter;

- (id)init
{
	self = [super init];
	if (self) {
		self.title = NSLocalizedString(@"Events", @"Default Title of EventListController");
		dateFormatter = [[FuzzyDateFormatter alloc] init];
		[dateFormatter setTimeStyle:NSDateFormatterShortStyle];
		eventViewController = nil;
		_service = nil;
		_events = [[NSMutableArray array] retain];
	}
	return self;
}

+ (EventListController*)forService: (Service *)ourService
{
	EventListController *eventListController = [[EventListController alloc] init];
	eventListController.service = ourService;

	return eventListController;
}

- (Service *)service
{
	return _service;
}

- (void)setService: (Service *)newService
{
	if(_service == newService) return;

	[_service release];
	_service = [newService retain];

	self.title = newService.sname;

	[_events removeAllObjects];
	[(UITableView *)self.view reloadData];
	[eventXMLDoc release];
	eventXMLDoc = nil;

	// Spawn a thread to fetch the event data so that the UI is not blocked while the
	// application parses the XML file.
	[NSThread detachNewThreadSelector:@selector(fetchEvents) toTarget:self withObject:nil];
}

- (void)dealloc
{
	[_events release];
	[_service release];
	[dateFormatter release];
	[eventViewController release];
	[eventXMLDoc release];

	[super dealloc];
}

- (void)didReceiveMemoryWarning
{
	[eventViewController release];
	eventViewController = nil;
	
    [super didReceiveMemoryWarning];
}

- (void)loadView
{
	UITableView *tableView = [[UITableView alloc] initWithFrame:[[UIScreen mainScreen] applicationFrame] style:UITableViewStylePlain];
	tableView.delegate = self;
	tableView.dataSource = self;
	tableView.rowHeight = 48.0;
	tableView.separatorStyle = UITableViewCellSeparatorStyleSingleLine;
	tableView.sectionHeaderHeight = 0;

	// setup our content view so that it auto-rotates along with the UViewController
	tableView.autoresizesSubviews = YES;
	tableView.autoresizingMask = (UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight);
	
	self.view = tableView;
	[tableView release];

	UIBarButtonItem *zapButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"Zap", @"") style:UIBarButtonItemStylePlain target:self action:@selector(zapAction:)];
	self.navigationItem.rightBarButtonItem = zapButton;
	[zapButton release];
}

- (void)zapAction:(id)sender
{
	[[RemoteConnectorObject sharedRemoteConnector] zapTo: _service];
}

- (void)fetchEvents
{
	NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
	[eventXMLDoc release];
	eventXMLDoc = [[[RemoteConnectorObject sharedRemoteConnector] fetchEPG: self action:@selector(addEvent:) service: _service] retain];
	[pool release];
}

- (void)addEvent:(id)event
{
	if(event != nil)
	{
		[(NSMutableArray *)_events addObject: event];
#ifdef ENABLE_LAGGY_ANIMATIONS
		[(UITableView*)self.view insertRowsAtIndexPaths: [NSArray arrayWithObject: [NSIndexPath indexPathForRow:[_events count]-1 inSection:0]]
						withRowAnimation: UITableViewRowAnimationTop];
	}
	else
#else
	}
#endif
	[(UITableView *)self.view reloadData];
}

#pragma mark	-
#pragma mark		Table View
#pragma mark	-

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
	EventTableViewCell *cell = (EventTableViewCell*)[tableView dequeueReusableCellWithIdentifier:kEventCell_ID];
	if(cell == nil)
		cell = [[[EventTableViewCell alloc] initWithFrame:CGRectZero reuseIdentifier:kEventCell_ID] autorelease];

	cell.formatter = dateFormatter;
	cell.event = (NSObject<EventProtocol> *)[_events objectAtIndex: indexPath.row];
	
	return cell;
}

- (NSIndexPath *)tableView:(UITableView *)tableView willSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
	NSObject<EventProtocol> *event = (NSObject<EventProtocol> *)[_events objectAtIndex: indexPath.row];

	if(eventViewController == nil)
		eventViewController = [[EventViewController alloc] init];

	eventViewController.event = event;
	eventViewController.service = _service;

	[self.navigationController pushViewController: eventViewController animated: YES];

	return nil;
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView 
{
	// TODO: seperate by day??
	return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section 
{
	return [_events count];
}

- (BOOL)shouldAutorotateToInterfaceOrientation: (UIInterfaceOrientation)interfaceOrientation
{
	return YES;
}

- (void)viewDidDisappear:(BOOL)animated
{
	[dateFormatter resetReferenceDate];
}

@end
