//
//  EventXMLReader.h
//  dreaMote
//
//  Created by Moritz Venn on 31.12.08.
//  Copyright 2008-2011 Moritz Venn. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "SaxXmlReader.h"

#import "EventSourceDelegate.h"
#import "NowNextSourceDelegate.h"

/*!
 @brief Enigma2 Event XML Reader.
 This XMLReader is implemented as streaming parser based on the SAX interface
 of libxml2.
 */
@interface Enigma2EventXMLReader : SaxXmlReader
{
@private
	SEL _delegateSelector; /*!< @brief Selector to perform on delegate. */
	NSObject *_delegate; /*!< @brief Delegate. */
	NSObject<EventProtocol> *_currentEvent;
}

/*!
 @brief Standard initializer.

 @param target Delegate.
 @return Enigma2EventXMLReader instance.
 */
- (id)initWithDelegate:(NSObject<EventSourceDelegate> *)delegate;

/*!
 @brief Standard initializer.

 @param target Delegate.
 @return Enigma2EventXMLReader instance.
 */
- (id)initWithNowDelegate:(NSObject<NowSourceDelegate> *)delegate;

/*!
 @brief Standard initializer.

 @param target Delegate.
 @return Enigma2EventXMLReader instance.
 */
- (id)initWithNextDelegate:(NSObject<NextSourceDelegate> *)delegate;

@end
