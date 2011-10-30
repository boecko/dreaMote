//
//  SearchHistoryListController.h
//  dreaMote
//
//  Created by Moritz Venn on 13.01.11.
//  Copyright 2011 Moritz Venn. All rights reserved.
//

#import <UIKit/UIKit.h>

@protocol SearchHistoryListDelegate;

@interface SearchHistoryListController : UIViewController <UITableViewDelegate, UITableViewDataSource>
{
@private
	NSMutableArray *_history; /*!< @brief Previously looked for strings. */
	NSObject<SearchHistoryListDelegate> *_historyDelegate; /*!< @brief Delegate. */
}

/*!
 @brief Add string to top of list.
 @note If the history already contains string it is moved to the top of the list

 @param new String to add.
 */
- (void)prepend:(NSString *)new;

/*!
 @brief Save history.
 */
- (void)saveHistory;

@property (nonatomic, strong) NSObject<SearchHistoryListDelegate> *historyDelegate;

@end

@protocol SearchHistoryListDelegate

/*!
 @brief Invoke a search

 @param text Text to search for.
 */
- (void)startSearch:(NSString *)text;

@end
