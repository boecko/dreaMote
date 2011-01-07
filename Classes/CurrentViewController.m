//
//  CurrentViewController.m
//  dreaMote
//
//  Created by Moritz Venn on 26.10.09.
//  Copyright 2009-2011 Moritz Venn. All rights reserved.
//

#import "CurrentViewController.h"

#import "FuzzyDateFormatter.h"
#import "RemoteConnectorObject.h"

#import "EventTableViewCell.h"
#import "ServiceTableViewCell.h"
#import "CellTextView.h"
#import "DisplayCell.h"
#import "Constants.h"

@interface  CurrentViewController()
- (UITextView *)create_Summary: (NSObject<EventProtocol> *)event;
@end

@implementation CurrentViewController

- (id)init
{
	if((self = [super init]))
	{
		self.title = NSLocalizedString(@"Currently playing", @"");
		self.tabBarItem.title = NSLocalizedString(@"Playing", @"TabBar Title of CurrentViewController");
		_dateFormatter = [[FuzzyDateFormatter alloc] init];
		[_dateFormatter setDateStyle:NSDateFormatterMediumStyle];
		[_dateFormatter setTimeStyle:NSDateFormatterShortStyle];
		_now = nil;
		_next = nil;
		_service = nil;
		_currentXMLDoc = nil;
	}
	
	return self;
}

- (void)dealloc
{
	[_now release];
	[_next release];
	[_service release];
	[_dateFormatter release];
	[_currentXMLDoc release];
	[_nowSummary release];
	[_nextSummary release];

	[super dealloc];
}

/* layout */
- (void)loadView
{
	// create table view
	_tableView = [[UITableView alloc] initWithFrame:[[UIScreen mainScreen] applicationFrame] style:UITableViewStyleGrouped];
	_tableView.separatorStyle = UITableViewCellSeparatorStyleSingleLine;
	_tableView.delegate = self;
	_tableView.dataSource = self;

	// setup our content view so that it auto-rotates along with the UViewController
	_tableView.autoresizesSubviews = YES;
	_tableView.autoresizingMask = (UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight);

	self.view = _tableView;

	// add header view
#if 0
	_refreshHeaderView = [[EGORefreshTableHeaderView alloc] initWithFrame:CGRectMake(0.0f, 0.0f - self.view.bounds.size.height, self.view.bounds.size.width, self.view.bounds.size.height)];
	_refreshHeaderView.delegate = self;
	[self.view addSubview:_refreshHeaderView];
#endif
}

- (UITextView *)create_Summary: (NSObject<EventProtocol> *)event
{
	UITextView *myTextView = [[UITextView alloc] initWithFrame:CGRectZero];
	myTextView.autoresizingMask = (UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight);
	myTextView.textColor = [UIColor blackColor];
	myTextView.font = [UIFont fontWithName:kFontName size:kTextViewFontSize];
	myTextView.editable = NO;
	
	NSString *description = event.edescription;
	if(description != nil)
		myTextView.text = description;
	else
		myTextView.text = @"";

	return [myTextView autorelease];
}

- (void)fetchData
{
	NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
	[_currentXMLDoc release];
	@try {
		_reloading = YES;
		_currentXMLDoc = [[[RemoteConnectorObject sharedRemoteConnector] getCurrent: self] retain];
	}
	@catch (NSException * e) {
		_currentXMLDoc = nil;
	}
	[pool release];
}

- (void)emptyData
{
	[_service release];
	_service = nil;
	[_now release];
	_now = nil;
	[_next release];
	_next = nil;
	NSIndexSet *idxSet = [NSIndexSet indexSetWithIndexesInRange:NSMakeRange(0, 3)];
	[_tableView reloadSections:idxSet withRowAnimation:UITableViewRowAnimationFade];
	[_currentXMLDoc release];
	_currentXMLDoc = nil;
}

- (void)addService: (NSObject<ServiceProtocol> *)service
{
	if(_service != nil)
		[_service release];
	_service = [service retain];

	[_refreshHeaderView egoRefreshScrollViewDataSourceDidFinishedLoading:_tableView];
	_reloading = NO;
	[_tableView reloadData];
}

- (void)addEvent: (NSObject<EventProtocol> *)event
{
	if(_now == nil)
	{
		_now = [event retain];
		_nowSummary = [[self create_Summary: _now] retain];
	}
	else
	{
		if(_next != nil)
			[_next release];
		_next = [event retain];
		_nextSummary = [[self create_Summary: _next] retain];
	}

	[_refreshHeaderView egoRefreshScrollViewDataSourceDidFinishedLoading:_tableView];
	_reloading = NO;
	[_tableView reloadData];
}

#pragma mark - UITableView delegates

- (NSIndexPath *)tableView:(UITableView *)tableView willSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
	return nil;
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
	return 3;
}

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section
{
	switch (section)
	{
		case 0:
			return NSLocalizedString(@"Service", @"");
		case 1:
			return (_now != nil) ? NSLocalizedString(@"Now", @"") : nil;
		case 2:
			return (_next != nil) ? NSLocalizedString(@"Next", @"") : nil;
		default:
			return nil;
	}
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
	switch(section)
	{
		case 0:
			return 1;
		case 1:
			if(_now == nil)
				return 0;
			return 2;
		case 2:
			if(_next == nil)
				return 0;
			return 2;
		default:
			return 0;
	}
}

// to determine specific row height for each cell, override this.  In this example, each row is determined
// buy the its subviews that are embedded.
//
- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
	switch (indexPath.section)
	{
		case 1:
		{
			if(_now == nil)
				return 0;
			if(indexPath.row == 1)
				return kTextViewHeight;
			break;
		}
		case 2:
		{
			if(_next == nil)
				return 0;
			if(indexPath.row == 1)
				return kTextViewHeight;
		}
		case 0:
		default:
			break;
	}
	
	return kUIRowHeight;
}

// to determine which UITableViewCell to be used on a given row.
//
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
	NSInteger section = indexPath.section;
	UITableViewCell *sourceCell = nil;

	// we are creating a new cell, setup its attributes
	switch(section)
	{
		case 0:
		{
			sourceCell = [tableView dequeueReusableCellWithIdentifier:kServiceCell_ID];
			if(sourceCell == nil)
				sourceCell = [[[ServiceTableViewCell alloc] initWithFrame:CGRectZero reuseIdentifier:kServiceCell_ID] autorelease];
			((ServiceTableViewCell *)sourceCell).service = _service;
			break;
		}
		case 1:
		{
			if(indexPath.row == 0)
			{
				sourceCell = [tableView dequeueReusableCellWithIdentifier:kEventCell_ID];
				if(sourceCell == nil)
					sourceCell = [[[EventTableViewCell alloc] initWithFrame:CGRectZero reuseIdentifier:kEventCell_ID] autorelease];
				((EventTableViewCell *)sourceCell).formatter = _dateFormatter;
				((EventTableViewCell *)sourceCell).event = _now;
				sourceCell.accessoryType = UITableViewCellAccessoryNone;
			}
			else
			{
				sourceCell = [tableView dequeueReusableCellWithIdentifier:kCellTextView_ID];
				if(sourceCell == nil)
					sourceCell = [[[CellTextView alloc] initWithFrame:CGRectZero reuseIdentifier:kCellTextView_ID] autorelease];
				
				((CellTextView *)sourceCell).view = _nowSummary;
				_nowSummary.backgroundColor = sourceCell.backgroundColor;
			}
			break;
		}
		case 2:
		{
			if(indexPath.row == 0)
			{
				sourceCell = [tableView dequeueReusableCellWithIdentifier:kEventCell_ID];
				if(sourceCell == nil)
					sourceCell = [[[EventTableViewCell alloc] initWithFrame:CGRectZero reuseIdentifier:kEventCell_ID] autorelease];
				((EventTableViewCell *)sourceCell).formatter = _dateFormatter;
				((EventTableViewCell *)sourceCell).event = _next;
				sourceCell.accessoryType = UITableViewCellAccessoryNone;
			}
			else
			{
				sourceCell = [tableView dequeueReusableCellWithIdentifier:kCellTextView_ID];
				if(sourceCell == nil)
					sourceCell = [[[CellTextView alloc] initWithFrame:CGRectZero reuseIdentifier:kCellTextView_ID] autorelease];
				
				((CellTextView *)sourceCell).view = _nextSummary;
				_nextSummary.backgroundColor = sourceCell.backgroundColor;
			}
			break;
		}
		default:
			break;
	}
	
	return sourceCell;
}

#pragma mark - UIViewController delegate methods

- (void)viewWillAppear:(BOOL)animated
{
	[_tableView reloadData];

	// Spawn a thread to fetch the event data so that the UI is not blocked while the
	// application parses the XML file.
	if([[RemoteConnectorObject sharedRemoteConnector] hasFeature: kFeaturesCurrent])
		[NSThread detachNewThreadSelector:@selector(fetchData) toTarget:self withObject:nil];
}

- (void)viewWillDisappear:(BOOL)animated
{
	[_service release];
	_service = nil;
	[_now release];
	_now = nil;
	[_next release];
	_next = nil;
	[_currentXMLDoc release];
	_currentXMLDoc = nil;
}

/* rotate with device */
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
	return YES;
}

@end
