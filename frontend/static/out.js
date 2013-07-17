function Isolate() {
  this._cachedBrowserPrefix = (void 0);
  this.instanceMap = (void 0);
  this.instanceMap2 = (void 0);
  this.instanceMap3 = (void 0);
  this.instanceMap4 = (void 0);
  this._getTypeNameOf = (void 0);
  this.NAME = 'TextComponentMediator';
  this.NAME2 = 'TextProxy';
  this.TEXT_CHANGED = 'text/changed';
}
init();

var $ = Isolate.prototype;
Isolate.$defineClass("Closure20", "Object",
function Closure() {
}, {
 toString$0: function() {
  return 'Closure';
 },
});

Isolate.$defineClass("_ChildNodeListLazy", "Object",
function _ChildNodeListLazy(_lib3_this) {
  this._lib3_this = _lib3_this;
}, {
 operator$index$1: function(index) {
  return $.index(this.get$_lib3_this().get$$dom_childNodes(), index);
 },
 get$length: function() {
  return $.get$length(this.get$_lib3_this().get$$dom_childNodes());
 },
 getRange$2: function(start, rangeLength) {
  return $._lib3_NodeListWrapper$1($.getRange2(this, start, rangeLength, []));
 },
 indexOf$2: function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 },
 isEmpty$0: function() {
  return $.eq($.get$length(this), 0);
 },
 filter$1: function(f) {
  return $._lib3_NodeListWrapper$1($.filter3(this, [], f));
 },
 forEach$1: function(f) {
  return $.forEach3(this, f);
 },
 iterator$0: function() {
  return $.iterator(this.get$_lib3_this().get$$dom_childNodes());
 },
 operator$indexSet$2: function(index, value) {
  this.get$_lib3_this().$dom_replaceChild$2(value, this.operator$index$1(index));
 },
 clear$0: function() {
  this.get$_lib3_this().set$text('');
 },
 removeLast$0: function() {
  var result = this.last$0();
  if (!$.eqNullB(result)) {
    this.get$_lib3_this().$dom_removeChild$1(result);
  }
  return result;
 },
 addAll$1: function(collection) {
  for (var t0 = $.iterator(collection); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    this.get$_lib3_this().$dom_appendChild$1(t1);
  }
 },
 add$1: function(value) {
  this.get$_lib3_this().$dom_appendChild$1(value);
 },
 last$0: function() {
  return this._this.lastChild;;
 },
 get$first: function() {
  return this._this.firstChild;;
 },
 first$0: function() { return this.get$first().$call$0(); },
 get$_lib3_this: function() { return this._lib3_this; },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("_AudioContextEventsImpl", "_EventsImpl",
function _AudioContextEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("Object", "",
function Object() {
}, {
 toString$0: function() {
  return $.objectToString(this);
 },
});

Isolate.$defineClass("MVCObserver", "Object",
function MVCObserver(notifyContext, notifyMethod) {
  this.notifyContext = notifyContext;
  this.notifyMethod = notifyMethod;
}, {
 notifyObserver$1: function(notification) {
  if (!$.eqNullB(this.get$notifyContext())) {
    this.getNotifyMethod$0().$call$1(notification);
  }
 },
 getNotifyMethod$0: function() {
  return this.get$notifyMethod();
 },
 get$notifyContext: function() { return this.notifyContext; },
 get$notifyMethod: function() { return this.notifyMethod; },
 MVCObserver$2: function(notifyMethod, notifyContext) {
 },
});

Isolate.$defineClass("MultitonModelExistsError", "Object",
function MultitonModelExistsError() {
}, {
 toString$0: function() {
  return 'IModel Multiton instance already constructed for this key.';
 },
});

Isolate.$defineClass("PrepareViewCommand", "MVCSimpleCommand",
function PrepareViewCommand(MVCNotifier_multitonKey) {
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 execute$1: function(note) {
  this.get$facade().registerMediator$1($.TextComponentMediator$1($.TextComponent$0()));
 },
});

Isolate.$defineClass("MultitonFacadeExistsError", "Object",
function MultitonFacadeExistsError() {
}, {
 toString$0: function() {
  return 'IFacade Multiton instance already constructed for this key.';
 },
});

Isolate.$defineClass("_NodeListWrapper", "_ListWrapper",
function _NodeListWrapper(_ListWrapper__lib3_list) {
  this._lib3_list = _ListWrapper__lib3_list;
}, {
 getRange$2: function(start, rangeLength) {
  return $._lib3_NodeListWrapper$1($.getRange(this.get$_lib3_list(), start, rangeLength));
 },
 filter$1: function(f) {
  return $._lib3_NodeListWrapper$1($.filter(this.get$_lib3_list(), f));
 },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("_AllMatchesIterable", "Object",
function _AllMatchesIterable(_lib_str, _lib_re) {
  this._lib_str = _lib_str;
  this._lib_re = _lib_re;
}, {
 iterator$0: function() {
  return $._lib_AllMatchesIterator$2(this.get$_lib_re(), this.get$_lib_str());
 },
 get$_lib_str: function() { return this._lib_str; },
 get$_lib_re: function() { return this._lib_re; },
});

Isolate.$defineClass("StartupCommand", "MVCMacroCommand",
function StartupCommand(MVCMacroCommand_subCommands, MVCNotifier_multitonKey) {
  this.subCommands = MVCMacroCommand_subCommands;
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 initializeMacroCommand$0: function() {
  this.addSubCommand$1(new $.Closure3());
  this.addSubCommand$1(new $.Closure4());
  this.addSubCommand$1(new $.Closure5());
 },
});

Isolate.$defineClass("MVCMacroCommand", "MVCNotifier",
function MVCMacroCommand() {
}, {
 set$subCommands: function(v) { this.subCommands = v; },
 get$subCommands: function() { return this.subCommands; },
 execute$1: function(note) {
  for (var t0 = $.iterator(this.get$subCommands()); t0.hasNext$0() === true; ) {
    var commandInstance = t0.next$0().$call$0();
    commandInstance.initializeNotifier$1(this.get$multitonKey());
    commandInstance.execute$1(note);
  }
 },
 addSubCommand$1: function(commandFactory) {
  $.add$1(this.get$subCommands(), commandFactory);
 },
 initializeMacroCommand$0: function() {
 },
 MVCMacroCommand$0: function() {
  var t0 = $.List((void 0));
  $.setRuntimeTypeInfo(t0, ({E: 'Function'}));
  this.set$subCommands(t0);
  this.initializeMacroCommand$0();
 },
});

Isolate.$defineClass("TextComponent", "Object",
function TextComponent(reverseButton, checkbox, textOutputLabel, textOutput, textInput, textForm) {
  this.reverseButton = reverseButton;
  this.checkbox = checkbox;
  this.textOutputLabel = textOutputLabel;
  this.textOutput = textOutput;
  this.textInput = textInput;
  this.textForm = textForm;
}, {
 dispatchTextChangedEvent$0: function() {
  var event$ = $.document().$dom_createEvent$1('HTMLEvents');
  event$.$dom_initEvent$3('text/changed', true, true);
  this.get$textForm().$dom_dispatchEvent$1(event$);
 },
 addEventListener$2: function(type, listener) {
  var t0 = ({});
  t0.listener_1 = listener;
  $.add$1($.index(this.get$textForm().get$on(), type), new $.Closure9(t0));
 },
 handleEvent$1: function(event$) {
  $0:{
    var t0 = event$.get$type();
    if ('keyup' === t0) {
      if (this.get$checkbox().get$checked() === true) {
        this.dispatchTextChangedEvent$0();
      }
      break $0;
    } else {
      if ('click' === t0) {
        event$.preventDefault$0();
        this.dispatchTextChangedEvent$0();
        break $0;
      }
    }
  }
 },
 get$inputText: function() {
  return this.get$textInput().get$value();
 },
 set$outputText: function(value) {
  this.set$isPalindrome(false);
  this.get$textOutput().set$value(value);
 },
 set$isPalindrome: function(izzit) {
  if (izzit === true) {
    this.get$textOutputLabel().set$innerHTML('Palindrome Detected');
  } else {
    this.get$textOutputLabel().set$innerHTML('Output Text');
  }
 },
 set$reverseButton: function(v) { this.reverseButton = v; },
 get$reverseButton: function() { return this.reverseButton; },
 set$checkbox: function(v) { this.checkbox = v; },
 get$checkbox: function() { return this.checkbox; },
 set$textOutputLabel: function(v) { this.textOutputLabel = v; },
 get$textOutputLabel: function() { return this.textOutputLabel; },
 set$textOutput: function(v) { this.textOutput = v; },
 get$textOutput: function() { return this.textOutput; },
 set$textInput: function(v) { this.textInput = v; },
 get$textInput: function() { return this.textInput; },
 set$textForm: function(v) { this.textForm = v; },
 get$textForm: function() { return this.textForm; },
 TextComponent$0: function() {
  this.set$textForm($.document().query$1('#textForm'));
  this.set$textInput($.document().query$1('#inputText'));
  this.set$textOutput($.document().query$1('#outputText'));
  this.set$textOutputLabel($.document().query$1('#outputTextLabel'));
  this.set$checkbox($.document().query$1('input[type=checkbox]'));
  this.set$reverseButton($.document().query$1('button[type=submit]'));
  $.add$1(this.get$checkbox().get$on().get$change(), new $.Closure13(this));
  $.add$1(this.get$reverseButton().get$on().get$click(), new $.Closure14(this));
  $.add$1(this.get$textInput().get$on().get$keyUp(), new $.Closure15(this));
 },
});

Isolate.$defineClass("ListIterator", "Object",
function ListIterator(list, i) {
  this.list = list;
  this.i = i;
}, {
 next$0: function() {
  if (!(this.hasNext$0() === true)) {
    throw $.captureStackTrace($.NoMoreElementsException$0());
  }
  var value = (this.get$list()[this.get$i()]);
  this.set$i($.add(this.get$i(), 1));
  return value;
 },
 hasNext$0: function() {
  return $.lt(this.get$i(), (this.get$list().length));
 },
 get$list: function() { return this.list; },
 set$i: function(v) { this.i = v; },
 get$i: function() { return this.i; },
});

Isolate.$defineClass("IllegalJSRegExpException", "Object",
function IllegalJSRegExpException(_lib2_errmsg, _lib2_pattern) {
  this._lib2_errmsg = _lib2_errmsg;
  this._lib2_pattern = _lib2_pattern;
}, {
 get$_lib2_errmsg: function() { return this._lib2_errmsg; },
 get$_lib2_pattern: function() { return this._lib2_pattern; },
 toString$0: function() {
  return 'IllegalJSRegExpException: \'' + $.stringToString(this.get$_lib2_pattern()) + '\' \'' + $.stringToString(this.get$_lib2_errmsg()) + '\'';
 },
});

Isolate.$defineClass("ProcessTextCommand", "MVCSimpleCommand",
function ProcessTextCommand(MVCNotifier_multitonKey) {
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 execute$1: function(note) {
  $.print('execute');
  var text = note.get$body();
  var chars = $.splitChars(text);
  if (typeof chars !== 'string' && (typeof chars !== 'object'||chars.constructor !== Array)) return this.execute$1$bailout(note, 1, text, chars);
  var buffer = $.StringBufferImpl$1('');
  for (var i = chars.length; i > 0; ) {
    var t0 = i - 1;
    var t1 = chars.length;
    if (t0 < 0 || t0 >= t1) throw $.ioore(t0);
    buffer.add$1(chars[t0]);
    i = t0;
  }
  var reverse = buffer.toString$0();
  this.get$facade().retrieveProxy$1($.NAME2).set$text(reverse);
  if ($.eqB(reverse, text) && !$.eqB(text, '')) {
    this.sendNotification$1('palindrome/detected');
  }
 },
 execute$1$bailout: function(note, state, env0, env1) {
  switch (state) {
    case 1:
      text = env0;
      chars = env1;
      break;
  }
  switch (state) {
    case 0:
      $.print('execute');
      var text = note.get$body();
      var chars = $.splitChars(text);
    case 1:
      state = 0;
      var buffer = $.StringBufferImpl$1('');
      var i = $.get$length(chars);
      L0: while (true) {
        if (!$.gtB(i, 0)) break L0;
        buffer.add$1($.index(chars, $.sub(i, 1)));
        i = $.sub(i, 1);
      }
      var reverse = buffer.toString$0();
      this.get$facade().retrieveProxy$1($.NAME2).set$text(reverse);
      if ($.eqB(reverse, text) && !$.eqB(text, '')) {
        this.sendNotification$1('palindrome/detected');
      }
  }
 },
});

Isolate.$defineClass("MultitonViewExistsError", "Object",
function MultitonViewExistsError() {
}, {
 toString$0: function() {
  return 'IViewMultiton instance already constructed for this key.';
 },
});

Isolate.$defineClass("NullPointerException", "Object",
function NullPointerException(arguments, functionName) {
  this.arguments = arguments;
  this.functionName = functionName;
}, {
 get$arguments: function() { return this.arguments; },
 get$functionName: function() { return this.functionName; },
 get$exceptionName: function() {
  return 'NullPointerException';
 },
 toString$0: function() {
  if ($.eqNullB(this.get$functionName())) {
    return this.get$exceptionName();
  } else {
    return '' + $.stringToString(this.get$exceptionName()) + ' : method: \'' + $.stringToString(this.get$functionName()) + '\'\nReceiver: null\nArguments: ' + $.stringToString(this.get$arguments());
  }
 },
});

Isolate.$defineClass("_WorkerEventsImpl", "_AbstractWorkerEventsImpl",
function _WorkerEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("FilteredElementList", "Object",
function FilteredElementList(_lib3_childNodes, _lib3_node) {
  this._lib3_childNodes = _lib3_childNodes;
  this._lib3_node = _lib3_node;
}, {
 last$0: function() {
  return $.last(this.get$_lib3_filtered());
 },
 indexOf$2: function(element, start) {
  return $.indexOf$2(this.get$_lib3_filtered(), element, start);
 },
 getRange$2: function(start, rangeLength) {
  return $.getRange(this.get$_lib3_filtered(), start, rangeLength);
 },
 iterator$0: function() {
  return $.iterator(this.get$_lib3_filtered());
 },
 operator$index$1: function(index) {
  return $.index(this.get$_lib3_filtered(), index);
 },
 get$length: function() {
  return $.get$length(this.get$_lib3_filtered());
 },
 isEmpty$0: function() {
  return $.isEmpty(this.get$_lib3_filtered());
 },
 filter$1: function(f) {
  return $.filter(this.get$_lib3_filtered(), f);
 },
 removeLast$0: function() {
  var result = this.last$0();
  if (!$.eqNullB(result)) {
    result.remove$0();
  }
  return result;
 },
 clear$0: function() {
  $.clear(this.get$_lib3_childNodes());
 },
 removeRange$2: function(start, rangeLength) {
  $.forEach($.getRange(this.get$_lib3_filtered(), start, rangeLength), new $.Closure12());
 },
 addAll$1: function(collection) {
  $.forEach(collection, this.get$add());
 },
 add$1: function(value) {
  $.add$1(this.get$_lib3_childNodes(), value);
 },
 get$add: function() { return new $.Closure21(this); },
 set$length: function(newLength) {
  var len = $.get$length(this);
  if ($.geB(newLength, len)) {
    return;
  } else {
    if ($.ltB(newLength, 0)) {
      throw $.captureStackTrace($.CTC5);
    }
  }
  this.removeRange$2($.sub(newLength, 1), $.sub(len, newLength));
 },
 operator$indexSet$2: function(index, value) {
  this.operator$index$1(index).replaceWith$1(value);
 },
 forEach$1: function(f) {
  $.forEach(this.get$_lib3_filtered(), f);
 },
 get$first: function() {
  for (var t0 = $.iterator(this.get$_lib3_childNodes()); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    if (typeof t1 === 'object' && t1.is$Element()) {
      return t1;
    }
  }
  return;
 },
 first$0: function() { return this.get$first().$call$0(); },
 get$_lib3_filtered: function() {
  return $.List$from($.filter(this.get$_lib3_childNodes(), new $.Closure10()));
 },
 get$_lib3_childNodes: function() { return this._lib3_childNodes; },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("_FixedSizeListIterator", "_VariableSizeListIterator",
function _FixedSizeListIterator(_lib3_length, _VariableSizeListIterator__lib3_pos, _VariableSizeListIterator__lib3_array) {
  this._lib3_length = _lib3_length;
  this._lib3_pos = _VariableSizeListIterator__lib3_pos;
  this._lib3_array = _VariableSizeListIterator__lib3_array;
}, {
 get$_lib3_length: function() { return this._lib3_length; },
 hasNext$0: function() {
  return $.gt(this.get$_lib3_length(), this.get$_lib3_pos());
 },
});

Isolate.$defineClass("JSSyntaxRegExp", "Object",
function JSSyntaxRegExp(ignoreCase, multiLine, pattern) {
  this.ignoreCase = ignoreCase;
  this.multiLine = multiLine;
  this.pattern = pattern;
}, {
 allMatches$1: function(str) {
  $.checkString(str);
  return $._lib_AllMatchesIterable$2(this, str);
 },
 hasMatch$1: function(str) {
  return $.regExpTest(this, $.checkString(str));
 },
 firstMatch$1: function(str) {
  var m = $.regExpExec(this, $.checkString(str));
  if (m === (void 0)) {
    return;
  }
  var matchStart = $.regExpMatchStart(m);
  var matchEnd = $.add(matchStart, $.get$length($.index(m, 0)));
  return $.MatchImplementation$5(this.get$pattern(), str, matchStart, matchEnd, m);
 },
 get$ignoreCase: function() { return this.ignoreCase; },
 get$multiLine: function() { return this.multiLine; },
 get$pattern: function() { return this.pattern; },
 JSSyntaxRegExp$_globalVersionOf$1: function(other) {
  $.regExpAttachGlobalNative(this);
 },
 is$JSSyntaxRegExp: true,
});

Isolate.$defineClass("_InputElementEventsImpl", "_ElementEventsImpl",
function _InputElementEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCSimpleCommand", "MVCNotifier",
function MVCSimpleCommand() {
}, {
 execute$1: function(note) {
 },
});

Isolate.$defineClass("_TextTrackListEventsImpl", "_EventsImpl",
function _TextTrackListEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_DeprecatedPeerConnectionEventsImpl", "_EventsImpl",
function _DeprecatedPeerConnectionEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCMediator", "MVCNotifier",
function MVCMediator() {
}, {
 get$viewComponent: function() { return this.viewComponent; },
 get$name: function() { return this.name; },
 onRegister$0: function() {
 },
 handleNotification$1: function(note) {
 },
 get$handleNotification: function() { return new $.Closure22(this); },
 listNotificationInterests$0: function() {
  var t0 = $.List((void 0));
  $.setRuntimeTypeInfo(t0, ({E: 'String'}));
  return t0;
 },
 getName$0: function() {
  return this.get$name();
 },
 MVCMediator$2: function(name$, viewComponent) {
 },
});

Isolate.$defineClass("ExceptionImplementation", "Object",
function ExceptionImplementation(_lib_msg) {
  this._lib_msg = _lib_msg;
}, {
 get$_lib_msg: function() { return this._lib_msg; },
 toString$0: function() {
  if (this.get$_lib_msg() === (void 0)) {
    var t0 = 'Exception';
  } else {
    t0 = 'Exception: ' + $.stringToString(this.get$_lib_msg());
  }
  return t0;
 },
});

Isolate.$defineClass("StringMatch", "Object",
function StringMatch(pattern, str, _lib4_start) {
  this.pattern = pattern;
  this.str = str;
  this._lib4_start = _lib4_start;
}, {
 get$pattern: function() { return this.pattern; },
 group$1: function(group_) {
  if (!$.eqB(group_, 0)) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(group_));
  }
  return this.get$pattern();
 },
 operator$index$1: function(g) {
  return this.group$1(g);
 },
});

Isolate.$defineClass("_DOMApplicationCacheEventsImpl", "_EventsImpl",
function _DOMApplicationCacheEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_EventListenerListImpl", "Object",
function _EventListenerListImpl(_lib3_type, _lib3_ptr) {
  this._lib3_type = _lib3_type;
  this._lib3_ptr = _lib3_ptr;
}, {
 _lib3_add$2: function(listener, useCapture) {
  this.get$_lib3_ptr().$dom_addEventListener$3(this.get$_lib3_type(), listener, useCapture);
 },
 add$2: function(listener, useCapture) {
  this._lib3_add$2(listener, useCapture);
  return this;
 },
 add$1: function(listener) {
  return this.add$2(listener,false)
},
 get$_lib3_type: function() { return this._lib3_type; },
 get$_lib3_ptr: function() { return this._lib3_ptr; },
});

Isolate.$defineClass("MVCModel", "Object",
function MVCModel(multitonKey, proxyMap) {
  this.multitonKey = multitonKey;
  this.proxyMap = proxyMap;
}, {
 set$multitonKey: function(v) { this.multitonKey = v; },
 get$multitonKey: function() { return this.multitonKey; },
 set$proxyMap: function(v) { this.proxyMap = v; },
 get$proxyMap: function() { return this.proxyMap; },
 retrieveProxy$1: function(proxyName) {
  return $.index(this.get$proxyMap(), proxyName);
 },
 registerProxy$1: function(proxy) {
  proxy.initializeNotifier$1(this.get$multitonKey());
  $.indexSet(this.get$proxyMap(), proxy.getName$0(), proxy);
  proxy.onRegister$0();
 },
 initializeModel$0: function() {
 },
 MVCModel$1: function(key) {
  if (!$.eqNullB($.index($.instanceMap4, key))) {
    throw $.captureStackTrace($.MultitonModelExistsError$0());
  }
  this.set$multitonKey(key);
  $.indexSet($.instanceMap4, this.get$multitonKey(), this);
  this.set$proxyMap($.HashMapImplementation$0());
  this.initializeModel$0();
 },
});

Isolate.$defineClass("_WindowEventsImpl", "_EventsImpl",
function _WindowEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
 get$keyUp: function() {
  return this._lib3_get$1('keyup');
 },
 get$click: function() {
  return this._lib3_get$1('click');
 },
 get$change: function() {
  return this._lib3_get$1('change');
 },
});

Isolate.$defineClass("_EventSourceEventsImpl", "_EventsImpl",
function _EventSourceEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_NotificationEventsImpl", "_EventsImpl",
function _NotificationEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
 get$click: function() {
  return this._lib3_get$1('click');
 },
});

Isolate.$defineClass("MVCView", "Object",
function MVCView(multitonKey, observerMap, mediatorMap) {
  this.multitonKey = multitonKey;
  this.observerMap = observerMap;
  this.mediatorMap = mediatorMap;
}, {
 set$multitonKey: function(v) { this.multitonKey = v; },
 get$multitonKey: function() { return this.multitonKey; },
 set$observerMap: function(v) { this.observerMap = v; },
 get$observerMap: function() { return this.observerMap; },
 set$mediatorMap: function(v) { this.mediatorMap = v; },
 get$mediatorMap: function() { return this.mediatorMap; },
 registerMediator$1: function(mediator) {
  if (!$.eqNullB($.index(this.get$mediatorMap(), mediator.getName$0()))) {
    return;
  }
  mediator.initializeNotifier$1(this.get$multitonKey());
  $.indexSet(this.get$mediatorMap(), mediator.getName$0(), mediator);
  var interests = mediator.listNotificationInterests$0();
  if (typeof interests !== 'string' && (typeof interests !== 'object'||interests.constructor !== Array)) return this.registerMediator$1$bailout(mediator, 1, interests);
  if (interests.length > 0) {
    var observer = $.MVCObserver$2(mediator.get$handleNotification(), mediator);
    for (var i = 0; i < interests.length; i = i + 1) {
      var t0 = interests.length;
      if (i < 0 || i >= t0) throw $.ioore(i);
      this.registerObserver$2(interests[i], observer);
    }
  }
  mediator.onRegister$0();
 },
 registerMediator$1$bailout: function(mediator, state, env0) {
  switch (state) {
    case 1:
      interests = env0;
      break;
  }
  switch (state) {
    case 0:
      if (!$.eqNullB($.index(this.get$mediatorMap(), mediator.getName$0()))) {
        return;
      }
      mediator.initializeNotifier$1(this.get$multitonKey());
      $.indexSet(this.get$mediatorMap(), mediator.getName$0(), mediator);
      var interests = mediator.listNotificationInterests$0();
    case 1:
      state = 0;
      if ($.gtB($.get$length(interests), 0)) {
        var observer = $.MVCObserver$2(mediator.get$handleNotification(), mediator);
        var i = 0;
        L0: while (true) {
          if (!$.ltB(i, $.get$length(interests))) break L0;
          this.registerObserver$2($.index(interests, i), observer);
          i = i + 1;
        }
      }
      mediator.onRegister$0();
  }
 },
 notifyObservers$1: function(note) {
  var observers_ref = $.index(this.get$observerMap(), note.getName$0());
  if (typeof observers_ref !== 'string' && (typeof observers_ref !== 'object'||observers_ref.constructor !== Array)) return this.notifyObservers$1$bailout(note, 1, observers_ref);
  if (!(observers_ref === (void 0))) {
    var observers = $.List((void 0));
    $.setRuntimeTypeInfo(observers, ({E: 'IObserver'}));
    for (var observer = (void 0), i = 0; i < observers_ref.length; i = i0) {
      var t0 = observers_ref.length;
      if (i < 0 || i >= t0) throw $.ioore(i);
      var t1 = observers_ref[i];
      observers.push(t1);
      observer = t1;
      var i0 = i + 1;
    }
    for (var observer0 = observer, i1 = 0; i1 < observers.length; i1 = i2) {
      var t2 = observers.length;
      if (i1 < 0 || i1 >= t2) throw $.ioore(i1);
      var t3 = observers[i1];
      t3.notifyObserver$1(note);
      observer0 = t3;
      var i2 = i1 + 1;
    }
  }
 },
 notifyObservers$1$bailout: function(note, state, env0) {
  switch (state) {
    case 1:
      observers_ref = env0;
      break;
  }
  switch (state) {
    case 0:
      var observers_ref = $.index(this.get$observerMap(), note.getName$0());
    case 1:
      state = 0;
      if (!$.eqNullB(observers_ref)) {
        var observers = $.List((void 0));
        $.setRuntimeTypeInfo(observers, ({E: 'IObserver'}));
        var observer = (void 0);
        var i = 0;
        L0: while (true) {
          if (!$.ltB(i, $.get$length(observers_ref))) break L0;
          var observer0 = $.index(observers_ref, i);
          observers.push(observer0);
          observer = observer0;
          var i0 = i + 1;
          i = i0;
        }
        var observer1 = observer;
        var i1 = 0;
        L1: while (true) {
          if (!(i1 < observers.length)) break L1;
          var t0 = observers.length;
          if (i1 < 0 || i1 >= t0) throw $.ioore(i1);
          var t1 = observers[i1];
          t1.notifyObserver$1(note);
          observer1 = t1;
          var i2 = i1 + 1;
          i1 = i2;
        }
      }
  }
 },
 registerObserver$2: function(noteName, observer) {
  if ($.eqNullB($.index(this.get$observerMap(), noteName))) {
    var t0 = this.get$observerMap();
    var t1 = $.List((void 0));
    $.setRuntimeTypeInfo(t1, ({E: 'IObserver'}));
    $.indexSet(t0, noteName, t1);
  }
  $.add$1($.index(this.get$observerMap(), noteName), observer);
 },
 initializeView$0: function() {
 },
 MVCView$1: function(key) {
  if (!$.eqNullB($.index($.instanceMap2, key))) {
    throw $.captureStackTrace($.MultitonViewExistsError$0());
  }
  this.set$multitonKey(key);
  $.indexSet($.instanceMap2, this.get$multitonKey(), this);
  this.set$mediatorMap($.HashMapImplementation$0());
  this.set$observerMap($.HashMapImplementation$0());
  this.initializeView$0();
 },
});

Isolate.$defineClass("_ListWrapper", "Object",
function _ListWrapper() {
}, {
 get$first: function() {
  return $.index(this.get$_lib3_list(), 0);
 },
 first$0: function() { return this.get$first().$call$0(); },
 getRange$2: function(start, rangeLength) {
  return $.getRange(this.get$_lib3_list(), start, rangeLength);
 },
 last$0: function() {
  return $.last(this.get$_lib3_list());
 },
 removeLast$0: function() {
  return $.removeLast(this.get$_lib3_list());
 },
 clear$0: function() {
  return $.clear(this.get$_lib3_list());
 },
 indexOf$2: function(element, start) {
  return $.indexOf$2(this.get$_lib3_list(), element, start);
 },
 addAll$1: function(collection) {
  return $.addAll(this.get$_lib3_list(), collection);
 },
 add$1: function(value) {
  return $.add$1(this.get$_lib3_list(), value);
 },
 set$length: function(newLength) {
  $.set$length(this.get$_lib3_list(), newLength);
 },
 operator$indexSet$2: function(index, value) {
  $.indexSet(this.get$_lib3_list(), index, value);
 },
 operator$index$1: function(index) {
  return $.index(this.get$_lib3_list(), index);
 },
 get$length: function() {
  return $.get$length(this.get$_lib3_list());
 },
 isEmpty$0: function() {
  return $.isEmpty(this.get$_lib3_list());
 },
 filter$1: function(f) {
  return $.filter(this.get$_lib3_list(), f);
 },
 forEach$1: function(f) {
  return $.forEach(this.get$_lib3_list(), f);
 },
 iterator$0: function() {
  return $.iterator(this.get$_lib3_list());
 },
 get$_lib3_list: function() { return this._lib3_list; },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("PrepareControllerCommand", "MVCSimpleCommand",
function PrepareControllerCommand(MVCNotifier_multitonKey) {
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 execute$1: function(note) {
  this.get$facade().registerCommand$2('process/input/text', new $.Closure16());
 },
});

Isolate.$defineClass("_PeerConnection00EventsImpl", "_EventsImpl",
function _PeerConnection00EventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCFacade", "Object",
function MVCFacade(multitonKey, view, model, controller) {
  this.multitonKey = multitonKey;
  this.view = view;
  this.model = model;
  this.controller = controller;
}, {
 set$multitonKey: function(v) { this.multitonKey = v; },
 get$multitonKey: function() { return this.multitonKey; },
 set$view: function(v) { this.view = v; },
 get$view: function() { return this.view; },
 set$model: function(v) { this.model = v; },
 get$model: function() { return this.model; },
 set$controller: function(v) { this.controller = v; },
 get$controller: function() { return this.controller; },
 initializeNotifier$1: function(key) {
  this.set$multitonKey(key);
 },
 notifyObservers$1: function(note) {
  if (!$.eqNullB(this.get$view())) {
    this.get$view().notifyObservers$1(note);
  }
 },
 registerObserver$2: function(noteName, observer) {
  this.get$view().registerObserver$2(noteName, observer);
 },
 sendNotification$3: function(noteName, body, type) {
  this.notifyObservers$1($.MVCNotification$3(noteName, body, type));
 },
 sendNotification$1: function(noteName) {
  return this.sendNotification$3(noteName,(void 0),(void 0))
},
 registerMediator$1: function(mediator) {
  if (!$.eqNullB(this.get$view())) {
    this.get$view().registerMediator$1(mediator);
  }
 },
 retrieveProxy$1: function(proxyName) {
  return this.get$model().retrieveProxy$1(proxyName);
 },
 registerProxy$1: function(proxy) {
  this.get$model().registerProxy$1(proxy);
 },
 registerCommand$2: function(noteName, commandFactory) {
  this.get$controller().registerCommand$2(noteName, commandFactory);
 },
 initializeView$0: function() {
  if (!$.eqNullB(this.get$view())) {
    return;
  }
  this.set$view($.getInstance2(this.get$multitonKey()));
 },
 initializeModel$0: function() {
  if (!$.eqNullB(this.get$model())) {
    return;
  }
  this.set$model($.getInstance4(this.get$multitonKey()));
 },
 initializeController$0: function() {
  if (!$.eqNullB(this.get$controller())) {
    return;
  }
  this.set$controller($.getInstance3(this.get$multitonKey()));
 },
 initializeFacade$0: function() {
  this.initializeModel$0();
  this.initializeController$0();
  this.initializeView$0();
 },
 MVCFacade$1: function(key) {
  if (!$.eqNullB($.index($.instanceMap, key))) {
    throw $.captureStackTrace($.MultitonFacadeExistsError$0());
  }
  this.initializeNotifier$1(key);
  $.indexSet($.instanceMap, this.get$multitonKey(), this);
  this.initializeFacade$0();
 },
});

Isolate.$defineClass("_ElementList", "_ListWrapper",
function _ElementList(_ListWrapper__lib3_list) {
  this._lib3_list = _ListWrapper__lib3_list;
}, {
 getRange$2: function(start, rangeLength) {
  return $._lib3_ElementList$1(Isolate.prototype._ListWrapper.prototype.getRange$2.call(this, start, rangeLength));
 },
 filter$1: function(f) {
  return $._lib3_ElementList$1(Isolate.prototype._ListWrapper.prototype.filter$1.call(this, f));
 },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("_WorkerContextEventsImpl", "_EventsImpl",
function _WorkerContextEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_DocumentEventsImpl", "_ElementEventsImpl",
function _DocumentEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
 get$keyUp: function() {
  return this._lib3_get$1('keyup');
 },
 get$click: function() {
  return this._lib3_get$1('click');
 },
 get$change: function() {
  return this._lib3_get$1('change');
 },
});

Isolate.$defineClass("MultitonControllerExistsError", "Object",
function MultitonControllerExistsError() {
}, {
 toString$0: function() {
  return 'IController Multiton instance already constructed for this key.';
 },
});

Isolate.$defineClass("IndexOutOfRangeException", "Object",
function IndexOutOfRangeException(_lib2_index) {
  this._lib2_index = _lib2_index;
}, {
 get$_lib2_index: function() { return this._lib2_index; },
 toString$0: function() {
  return 'IndexOutOfRangeException: ' + $.stringToString(this.get$_lib2_index());
 },
});

Isolate.$defineClass("Closure18", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$2: function(key, value) {
  this.box_0.f_1.$call$1(key);
 },
});

Isolate.$defineClass("Closure19", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$2: function(key, value) {
  if (this.box_0.f_1.$call$1(key) === true) {
    $.add$1(this.box_0.result_2, key);
  }
 },
});

Isolate.$defineClass("Closure", "Closure20",
function Closure() {
}, {
 $call$0: function() {
  return $.StartupCommand$0();
 },
});

Isolate.$defineClass("_BatteryManagerEventsImpl", "_EventsImpl",
function _BatteryManagerEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_EventsImpl", "Object",
function _EventsImpl(_lib3_ptr) {
  this._lib3_ptr = _lib3_ptr;
}, {
 _lib3_get$1: function(type) {
  return $._lib3_EventListenerListImpl$2(this.get$_lib3_ptr(), type);
 },
 operator$index$1: function(type) {
  return this._lib3_get$1($.toLowerCase(type));
 },
 get$_lib3_ptr: function() { return this._lib3_ptr; },
});

Isolate.$defineClass("Closure2", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$2: function(k, v) {
  if (!(this.box_0.first_3 === true)) {
    $.add$1(this.box_0.result_1, ', ');
  }
  this.box_0.first_3 = false;
  $._emitObject(k, this.box_0.result_1, this.box_0.visiting_2);
  $.add$1(this.box_0.result_1, ': ');
  $._emitObject(v, this.box_0.result_1, this.box_0.visiting_2);
 },
});

Isolate.$defineClass("HashSetImplementation", "Object",
function HashSetImplementation(_lib_backingMap) {
  this._lib_backingMap = _lib_backingMap;
}, {
 set$_lib_backingMap: function(v) { this._lib_backingMap = v; },
 get$_lib_backingMap: function() { return this._lib_backingMap; },
 toString$0: function() {
  return $.collectionToString(this);
 },
 iterator$0: function() {
  var t0 = $.HashSetIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({E: 'E'}));
  return t0;
 },
 get$length: function() {
  return $.get$length(this.get$_lib_backingMap());
 },
 isEmpty$0: function() {
  return $.isEmpty(this.get$_lib_backingMap());
 },
 filter$1: function(f) {
  var t0 = ({});
  t0.f_1 = f;
  var result = $.HashSetImplementation$0();
  $.setRuntimeTypeInfo(result, ({E: 'E'}));
  t0.result_2 = result;
  $.forEach(this.get$_lib_backingMap(), new $.Closure19(t0));
  return t0.result_2;
 },
 forEach$1: function(f) {
  var t0 = ({});
  t0.f_1 = f;
  $.forEach(this.get$_lib_backingMap(), new $.Closure18(t0));
 },
 addAll$1: function(collection) {
  $.forEach(collection, new $.Closure17(this));
 },
 contains$1: function(value) {
  return this.get$_lib_backingMap().containsKey$1(value);
 },
 add$1: function(value) {
  $.indexSet(this.get$_lib_backingMap(), value, value);
 },
 clear$0: function() {
  $.clear(this.get$_lib_backingMap());
 },
 HashSetImplementation$0: function() {
  this.set$_lib_backingMap($.HashMapImplementation$0());
 },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("Closure3", "Closure20",
function Closure() {
}, {
 $call$0: function() {
  return $.PrepareControllerCommand$0();
 },
});

Isolate.$defineClass("_TextTrackEventsImpl", "_EventsImpl",
function _TextTrackEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_IDBRequestEventsImpl", "_EventsImpl",
function _IDBRequestEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("Closure4", "Closure20",
function Closure() {
}, {
 $call$0: function() {
  return $.PrepareModelCommand$0();
 },
});

Isolate.$defineClass("MVCNotification", "Object",
function MVCNotification(body, type, name) {
  this.body = body;
  this.type = type;
  this.name = name;
}, {
 get$body: function() { return this.body; },
 get$type: function() { return this.type; },
 get$name: function() { return this.name; },
 getName$0: function() {
  return this.get$name();
 },
 MVCNotification$3: function(name$, body, type) {
 },
});

Isolate.$defineClass("_SpeechRecognitionEventsImpl", "_EventsImpl",
function _SpeechRecognitionEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_SVGElementInstanceEventsImpl", "_EventsImpl",
function _SVGElementInstanceEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
 get$keyUp: function() {
  return this._lib3_get$1('keyup');
 },
 get$click: function() {
  return this._lib3_get$1('click');
 },
 get$change: function() {
  return this._lib3_get$1('change');
 },
});

Isolate.$defineClass("_WebSocketEventsImpl", "_EventsImpl",
function _WebSocketEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_VariableSizeListIterator", "Object",
function _VariableSizeListIterator() {
}, {
 set$_lib3_pos: function(v) { this._lib3_pos = v; },
 get$_lib3_pos: function() { return this._lib3_pos; },
 get$_lib3_array: function() { return this._lib3_array; },
 next$0: function() {
  if (!(this.hasNext$0() === true)) {
    throw $.captureStackTrace($.CTC3);
  }
  var t0 = this.get$_lib3_array();
  var t1 = this.get$_lib3_pos();
  this.set$_lib3_pos($.add(t1, 1));
  return $.index(t0, t1);
 },
 hasNext$0: function() {
  return $.gt($.get$length(this.get$_lib3_array()), this.get$_lib3_pos());
 },
});

Isolate.$defineClass("MetaInfo", "Object",
function MetaInfo(set, tags, tag) {
  this.set = set;
  this.tags = tags;
  this.tag = tag;
}, {
 get$set: function() { return this.set; },
 get$tag: function() { return this.tag; },
});

Isolate.$defineClass("Closure5", "Closure20",
function Closure() {
}, {
 $call$0: function() {
  return $.PrepareViewCommand$0();
 },
});

Isolate.$defineClass("_MediaStreamEventsImpl", "_EventsImpl",
function _MediaStreamEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("NotifierLacksMultitonKeyError", "Object",
function NotifierLacksMultitonKeyError() {
}, {
 toString$0: function() {
  return 'multitonKey for this Notifier not yet initialized!';
 },
});

Isolate.$defineClass("Closure6", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$0: function() {
  return this.box_0.closure_1.$call$0();
 },
});

Isolate.$defineClass("Closure7", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$0: function() {
  return this.box_0.closure_1.$call$1(this.box_0.arg1_2);
 },
});

Isolate.$defineClass("Closure8", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$0: function() {
  return this.box_0.closure_1.$call$2(this.box_0.arg1_2, this.box_0.arg2_3);
 },
});

Isolate.$defineClass("ObjectNotClosureException", "Object",
function ObjectNotClosureException() {
}, {
 toString$0: function() {
  return 'Object is not closure';
 },
});

Isolate.$defineClass("PrepareModelCommand", "MVCSimpleCommand",
function PrepareModelCommand(MVCNotifier_multitonKey) {
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 execute$1: function(note) {
  this.get$facade().registerProxy$1($.TextProxy$0());
 },
});

Isolate.$defineClass("Closure9", "Closure20",
function Closure(box_0) {
  this.box_0 = box_0;
}, {
 $call$1: function(event$) {
  return this.box_0.listener_1.$call$1(event$);
 },
});

Isolate.$defineClass("Closure10", "Closure20",
function Closure() {
}, {
 $call$1: function(n) {
  return typeof n === 'object' && n.is$Element();
 },
});

Isolate.$defineClass("_ChildrenElementList", "Object",
function _ChildrenElementList(_lib3_childElements, _lib3_element) {
  this._lib3_childElements = _lib3_childElements;
  this._lib3_element = _lib3_element;
}, {
 last$0: function() {
  return this.get$_lib3_element().get$$dom_lastElementChild();
 },
 removeLast$0: function() {
  var result = this.last$0();
  if (!$.eqNullB(result)) {
    this.get$_lib3_element().$dom_removeChild$1(result);
  }
  return result;
 },
 clear$0: function() {
  this.get$_lib3_element().set$text('');
 },
 indexOf$2: function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 },
 getRange$2: function(start, rangeLength) {
  return $._lib3_FrozenElementList$_wrap$1($.getRange2(this, start, rangeLength, []));
 },
 addAll$1: function(collection) {
  for (var t0 = $.iterator(collection); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    this.get$_lib3_element().$dom_appendChild$1(t1);
  }
 },
 iterator$0: function() {
  return $.iterator(this._lib3_toList$0());
 },
 add$1: function(value) {
  this.get$_lib3_element().$dom_appendChild$1(value);
  return value;
 },
 set$length: function(newLength) {
  throw $.captureStackTrace($.CTC4);
 },
 operator$indexSet$2: function(index, value) {
  this.get$_lib3_element().$dom_replaceChild$2(value, $.index(this.get$_lib3_childElements(), index));
 },
 operator$index$1: function(index) {
  return $.index(this.get$_lib3_childElements(), index);
 },
 get$length: function() {
  return $.get$length(this.get$_lib3_childElements());
 },
 isEmpty$0: function() {
  return $.eqNull(this.get$_lib3_element().get$$dom_firstElementChild());
 },
 filter$1: function(f) {
  var t0 = ({});
  t0.f_1 = f;
  var output = [];
  this.forEach$1(new $.Closure11(t0, output));
  return $._lib3_FrozenElementList$_wrap$1(output);
 },
 forEach$1: function(f) {
  for (var t0 = $.iterator(this.get$_lib3_childElements()); t0.hasNext$0() === true; ) {
    f.$call$1(t0.next$0());
  }
 },
 get$first: function() {
  return this.get$_lib3_element().get$$dom_firstElementChild();
 },
 first$0: function() { return this.get$first().$call$0(); },
 _lib3_toList$0: function() {
  var output = $.List($.get$length(this.get$_lib3_childElements()));
  var len = $.get$length(this.get$_lib3_childElements());
  if (typeof len !== 'number') return this._lib3_toList$0$bailout(1, output, len);
  var i = 0;
  for (; i < len; i = i + 1) {
    var t0 = $.index(this.get$_lib3_childElements(), i);
    var t1 = output.length;
    if (i < 0 || i >= t1) throw $.ioore(i);
    output[i] = t0;
  }
  return output;
 },
 _lib3_toList$0$bailout: function(state, env0, env1) {
  switch (state) {
    case 1:
      output = env0;
      len = env1;
      break;
  }
  switch (state) {
    case 0:
      var output = $.List($.get$length(this.get$_lib3_childElements()));
      var len = $.get$length(this.get$_lib3_childElements());
    case 1:
      state = 0;
      var i = 0;
      L0: while (true) {
        if (!$.ltB(i, len)) break L0;
        var t0 = $.index(this.get$_lib3_childElements(), i);
        var t1 = output.length;
        if (i < 0 || i >= t1) throw $.ioore(i);
        output[i] = t0;
        i = i + 1;
      }
      return output;
  }
 },
 get$_lib3_childElements: function() { return this._lib3_childElements; },
 get$_lib3_element: function() { return this._lib3_element; },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("Closure11", "Closure20",
function Closure(box_0, output_2) {
  this.box_0 = box_0;
  this.output_2 = output_2;
}, {
 $call$1: function(element) {
  if (this.box_0.f_1.$call$1(element) === true) {
    $.add$1(this.output_2, element);
  }
 },
});

Isolate.$defineClass("Closure12", "Closure20",
function Closure() {
}, {
 $call$1: function(el) {
  return el.remove$0();
 },
});

Isolate.$defineClass("Closure13", "Closure20",
function Closure(this_0) {
  this.this_0 = this_0;
}, {
 $call$1: function(event$) {
  return this.this_0.handleEvent$1(event$);
 },
});

Isolate.$defineClass("_DeletedKeySentinel", "Object",
function _DeletedKeySentinel() {
}, {
});

Isolate.$defineClass("_FrozenElementListIterator", "Object",
function _FrozenElementListIterator(_lib3_index, _lib3_list) {
  this._lib3_index = _lib3_index;
  this._lib3_list = _lib3_list;
}, {
 hasNext$0: function() {
  return $.lt(this.get$_lib3_index(), $.get$length(this.get$_lib3_list()));
 },
 next$0: function() {
  if (!(this.hasNext$0() === true)) {
    throw $.captureStackTrace($.CTC3);
  }
  var t0 = this.get$_lib3_list();
  var t1 = this.get$_lib3_index();
  this.set$_lib3_index($.add(t1, 1));
  return $.index(t0, t1);
 },
 set$_lib3_index: function(v) { this._lib3_index = v; },
 get$_lib3_index: function() { return this._lib3_index; },
 get$_lib3_list: function() { return this._lib3_list; },
});

Isolate.$defineClass("TextComponentMediator", "MVCMediator",
function TextComponentMediator(MVCMediator_viewComponent, MVCMediator_name, MVCNotifier_multitonKey) {
  this.viewComponent = MVCMediator_viewComponent;
  this.name = MVCMediator_name;
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 handleNotification$1: function(note) {
  $0:{
    var t0 = note.get$name();
    if ($.eqB($.TEXT_CHANGED, t0)) {
      var t1 = note.get$body();
      this.get$textComponent().set$outputText(t1);
      break $0;
    } else {
      if ('palindrome/detected' === t0) {
        this.get$textComponent().set$isPalindrome(true);
        break $0;
      }
    }
  }
 },
 get$handleNotification: function() { return new $.Closure25(this); },
 handleEvent$1: function(event$) {
  $.print('hhh');
  $0:{
    if ('text/changed' === event$.get$type()) {
      this.sendNotification$2('process/input/text', this.get$textComponent().get$inputText());
      break $0;
    }
  }
 },
 get$handleEvent: function() { return new $.Closure26(this); },
 listNotificationInterests$0: function() {
  return ['palindrome/detected', $.TEXT_CHANGED];
 },
 onRegister$0: function() {
  $.print('text/changed');
  this.get$textComponent().addEventListener$2('text/changed', this.get$handleEvent());
 },
 get$textComponent: function() {
  return this.get$viewComponent();
 },
 TextComponentMediator$1: function(viewComponent) {
 },
});

Isolate.$defineClass("Closure14", "Closure20",
function Closure(this_1) {
  this.this_1 = this_1;
}, {
 $call$1: function(event$) {
  return this.this_1.handleEvent$1(event$);
 },
});

Isolate.$defineClass("_XMLHttpRequestEventsImpl", "_EventsImpl",
function _XMLHttpRequestEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_JavaScriptAudioNodeEventsImpl", "_EventsImpl",
function _JavaScriptAudioNodeEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("TextProxy", "MVCProxy",
function TextProxy(MVCProxy_data, MVCProxy_name, MVCNotifier_multitonKey) {
  this.data = MVCProxy_data;
  this.name = MVCProxy_name;
  this.multitonKey = MVCNotifier_multitonKey;
}, {
 set$text: function(t) {
  $.print('setdata');
  this.setData$1(t);
  this.sendNotification$2($.TEXT_CHANGED, this.get$text());
 },
 get$text: function() {
  return this.get$data();
 },
 TextProxy$0: function() {
 },
});

Isolate.$defineClass("_IDBDatabaseEventsImpl", "_EventsImpl",
function _IDBDatabaseEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCProxy", "MVCNotifier",
function MVCProxy() {
}, {
 set$data: function(v) { this.data = v; },
 get$data: function() { return this.data; },
 get$name: function() { return this.name; },
 onRegister$0: function() {
 },
 setData$1: function(dataObject) {
  this.set$data(dataObject);
 },
 getName$0: function() {
  return this.get$name();
 },
 MVCProxy$2: function(name$, data) {
 },
});

Isolate.$defineClass("_MessagePortEventsImpl", "_EventsImpl",
function _MessagePortEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_TextTrackCueEventsImpl", "_EventsImpl",
function _TextTrackCueEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("Closure15", "Closure20",
function Closure(this_2) {
  this.this_2 = this_2;
}, {
 $call$1: function(event$) {
  return this.this_2.handleEvent$1(event$);
 },
});

Isolate.$defineClass("_ElementEventsImpl", "_EventsImpl",
function _ElementEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
 get$keyUp: function() {
  return this._lib3_get$1('keyup');
 },
 get$click: function() {
  return this._lib3_get$1('click');
 },
 get$change: function() {
  return this._lib3_get$1('change');
 },
});

Isolate.$defineClass("Closure16", "Closure20",
function Closure() {
}, {
 $call$0: function() {
  return $.ProcessTextCommand$0();
 },
});

Isolate.$defineClass("MatchImplementation", "Object",
function MatchImplementation(_lib_groups, _lib_end, _lib_start, str, pattern) {
  this._lib_groups = _lib_groups;
  this._lib_end = _lib_end;
  this._lib_start = _lib_start;
  this.str = str;
  this.pattern = pattern;
}, {
 operator$index$1: function(index) {
  return this.group$1(index);
 },
 group$1: function(index) {
  return $.index(this.get$_lib_groups(), index);
 },
 get$_lib_groups: function() { return this._lib_groups; },
 get$pattern: function() { return this.pattern; },
});

Isolate.$defineClass("_XMLHttpRequestUploadEventsImpl", "_EventsImpl",
function _XMLHttpRequestUploadEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCController", "Object",
function MVCController(multitonKey, commandMap, view) {
  this.multitonKey = multitonKey;
  this.commandMap = commandMap;
  this.view = view;
}, {
 set$multitonKey: function(v) { this.multitonKey = v; },
 get$multitonKey: function() { return this.multitonKey; },
 set$commandMap: function(v) { this.commandMap = v; },
 get$commandMap: function() { return this.commandMap; },
 set$view: function(v) { this.view = v; },
 get$view: function() { return this.view; },
 registerCommand$2: function(noteName, commandFactory) {
  if ($.eqNullB($.index(this.get$commandMap(), noteName))) {
    this.get$view().registerObserver$2(noteName, $.MVCObserver$2(this.get$executeCommand(), this));
  }
  $.indexSet(this.get$commandMap(), noteName, commandFactory);
 },
 executeCommand$1: function(note) {
  var commandFactory = $.index(this.get$commandMap(), note.getName$0());
  if ($.eqNullB(commandFactory)) {
    return;
  }
  var commandInstance = commandFactory.$call$0();
  commandInstance.initializeNotifier$1(this.get$multitonKey());
  commandInstance.execute$1(note);
 },
 get$executeCommand: function() { return new $.Closure27(this); },
 initializeController$0: function() {
  this.set$view($.getInstance2(this.get$multitonKey()));
 },
 MVCController$1: function(key) {
  if (!$.eqNullB($.index($.instanceMap3, key))) {
    throw $.captureStackTrace($.MultitonControllerExistsError$0());
  }
  this.set$multitonKey(key);
  $.indexSet($.instanceMap3, this.get$multitonKey(), this);
  this.set$commandMap($.HashMapImplementation$0());
  this.initializeController$0();
 },
});

Isolate.$defineClass("UnsupportedOperationException", "Object",
function UnsupportedOperationException(_lib2_message) {
  this._lib2_message = _lib2_message;
}, {
 get$_lib2_message: function() { return this._lib2_message; },
 toString$0: function() {
  return 'UnsupportedOperationException: ' + $.stringToString(this.get$_lib2_message());
 },
});

Isolate.$defineClass("_DedicatedWorkerContextEventsImpl", "_WorkerContextEventsImpl",
function _DedicatedWorkerContextEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("StackOverflowException", "Object",
function StackOverflowException() {
}, {
 toString$0: function() {
  return 'Stack Overflow';
 },
});

Isolate.$defineClass("StringBufferImpl", "Object",
function StringBufferImpl(_lib_length, _lib_buffer) {
  this._lib_length = _lib_length;
  this._lib_buffer = _lib_buffer;
}, {
 set$_lib_length: function(v) { this._lib_length = v; },
 get$_lib_length: function() { return this._lib_length; },
 set$_lib_buffer: function(v) { this._lib_buffer = v; },
 get$_lib_buffer: function() { return this._lib_buffer; },
 toString$0: function() {
  if ($.get$length(this.get$_lib_buffer()) === 0) {
    return '';
  }
  if ($.get$length(this.get$_lib_buffer()) === 1) {
    return $.index(this.get$_lib_buffer(), 0);
  }
  var result = $.concatAll(this.get$_lib_buffer());
  $.clear(this.get$_lib_buffer());
  $.add$1(this.get$_lib_buffer(), result);
  return result;
 },
 clear$0: function() {
  var t0 = $.List((void 0));
  $.setRuntimeTypeInfo(t0, ({E: 'String'}));
  this.set$_lib_buffer(t0);
  this.set$_lib_length(0);
  return this;
 },
 addAll$1: function(objects) {
  for (var t0 = $.iterator(objects); t0.hasNext$0() === true; ) {
    this.add$1(t0.next$0());
  }
  return this;
 },
 add$1: function(obj) {
  var str = $.toString(obj);
  if (str === (void 0) || $.isEmpty(str) === true) {
    return this;
  }
  $.add$1(this.get$_lib_buffer(), str);
  this.set$_lib_length($.add(this.get$_lib_length(), $.get$length(str)));
  return this;
 },
 isEmpty$0: function() {
  return this.get$_lib_length() === 0;
 },
 get$length: function() {
  return this.get$_lib_length();
 },
 StringBufferImpl$1: function(content$) {
  this.clear$0();
  this.add$1(content$);
 },
});

Isolate.$defineClass("HashMapImplementation", "Object",
function HashMapImplementation(_lib_numberOfDeleted, _lib_numberOfEntries, _lib_loadLimit, _lib_values, _lib_keys) {
  this._lib_numberOfDeleted = _lib_numberOfDeleted;
  this._lib_numberOfEntries = _lib_numberOfEntries;
  this._lib_loadLimit = _lib_loadLimit;
  this._lib_values = _lib_values;
  this._lib_keys = _lib_keys;
}, {
 toString$0: function() {
  return $.mapToString(this);
 },
 containsKey$1: function(key) {
  return !$.eqB(this._lib_probeForLookup$1(key), -1);
 },
 forEach$1: function(f) {
  var length$ = $.get$length(this.get$_lib_keys());
  if (typeof length$ !== 'number') return this.forEach$1$bailout(f, 1, length$);
  for (var i = 0; i < length$; i = i + 1) {
    var key = $.index(this.get$_lib_keys(), i);
    if (!(key === (void 0)) && !(key === $.CTC2)) {
      f.$call$2(key, $.index(this.get$_lib_values(), i));
    }
  }
 },
 forEach$1$bailout: function(f, state, env0) {
  switch (state) {
    case 1:
      length$ = env0;
      break;
  }
  switch (state) {
    case 0:
      var length$ = $.get$length(this.get$_lib_keys());
    case 1:
      state = 0;
      var i = 0;
      L0: while (true) {
        if (!$.ltB(i, length$)) break L0;
        var key = $.index(this.get$_lib_keys(), i);
        if (!(key === (void 0)) && !(key === $.CTC2)) {
          f.$call$2(key, $.index(this.get$_lib_values(), i));
        }
        i = i + 1;
      }
  }
 },
 get$length: function() {
  return this.get$_lib_numberOfEntries();
 },
 isEmpty$0: function() {
  return $.eq(this.get$_lib_numberOfEntries(), 0);
 },
 operator$index$1: function(key) {
  var index = this._lib_probeForLookup$1(key);
  if ($.ltB(index, 0)) {
    return;
  }
  return $.index(this.get$_lib_values(), index);
 },
 operator$indexSet$2: function(key, value) {
  this._lib_ensureCapacity$0();
  var index = this._lib_probeForAdding$1(key);
  if ($.index(this.get$_lib_keys(), index) === (void 0) || $.index(this.get$_lib_keys(), index) === $.CTC2) {
    this.set$_lib_numberOfEntries($.add(this.get$_lib_numberOfEntries(), 1));
  }
  $.indexSet(this.get$_lib_keys(), index, key);
  $.indexSet(this.get$_lib_values(), index, value);
 },
 clear$0: function() {
  this.set$_lib_numberOfEntries(0);
  this.set$_lib_numberOfDeleted(0);
  var length$ = $.get$length(this.get$_lib_keys());
  if (typeof length$ !== 'number') return this.clear$0$bailout(1, length$);
  for (var i = 0; i < length$; i = i + 1) {
    $.indexSet(this.get$_lib_keys(), i, (void 0));
    $.indexSet(this.get$_lib_values(), i, (void 0));
  }
 },
 clear$0$bailout: function(state, env0) {
  switch (state) {
    case 1:
      length$ = env0;
      break;
  }
  switch (state) {
    case 0:
      this.set$_lib_numberOfEntries(0);
      this.set$_lib_numberOfDeleted(0);
      var length$ = $.get$length(this.get$_lib_keys());
    case 1:
      state = 0;
      var i = 0;
      L0: while (true) {
        if (!$.ltB(i, length$)) break L0;
        $.indexSet(this.get$_lib_keys(), i, (void 0));
        $.indexSet(this.get$_lib_values(), i, (void 0));
        i = i + 1;
      }
  }
 },
 _lib_grow$1: function(newCapacity) {
  $.assert($._isPowerOfTwo(newCapacity));
  var capacity = $.get$length(this.get$_lib_keys());
  if (typeof capacity !== 'number') return this._lib_grow$1$bailout(newCapacity, 1, capacity);
  this.set$_lib_loadLimit($._computeLoadLimit(newCapacity));
  var oldKeys = this.get$_lib_keys();
  if (typeof oldKeys !== 'string' && (typeof oldKeys !== 'object'||oldKeys.constructor !== Array)) return this._lib_grow$1$bailout(newCapacity, 2, capacity, oldKeys);
  var oldValues = this.get$_lib_values();
  if (typeof oldValues !== 'string' && (typeof oldValues !== 'object'||oldValues.constructor !== Array)) return this._lib_grow$1$bailout(newCapacity, 3, capacity, oldKeys, oldValues);
  this.set$_lib_keys($.List(newCapacity));
  var t0 = $.List(newCapacity);
  $.setRuntimeTypeInfo(t0, ({E: 'V'}));
  this.set$_lib_values(t0);
  for (var i = 0; i < capacity; i = i + 1) {
    var t1 = oldKeys.length;
    if (i < 0 || i >= t1) throw $.ioore(i);
    var t2 = oldKeys[i];
    if (t2 === (void 0) || t2 === $.CTC2) {
      continue;
    }
    var t3 = oldValues.length;
    if (i < 0 || i >= t3) throw $.ioore(i);
    var t4 = oldValues[i];
    var newIndex = this._lib_probeForAdding$1(t2);
    $.indexSet(this.get$_lib_keys(), newIndex, t2);
    $.indexSet(this.get$_lib_values(), newIndex, t4);
  }
  this.set$_lib_numberOfDeleted(0);
 },
 _lib_grow$1$bailout: function(newCapacity, state, env0, env1, env2) {
  switch (state) {
    case 1:
      capacity = env0;
      break;
    case 2:
      capacity = env0;
      oldKeys = env1;
      break;
    case 3:
      capacity = env0;
      oldKeys = env1;
      oldValues = env2;
      break;
  }
  switch (state) {
    case 0:
      $.assert($._isPowerOfTwo(newCapacity));
      var capacity = $.get$length(this.get$_lib_keys());
    case 1:
      state = 0;
      this.set$_lib_loadLimit($._computeLoadLimit(newCapacity));
      var oldKeys = this.get$_lib_keys();
    case 2:
      state = 0;
      var oldValues = this.get$_lib_values();
    case 3:
      state = 0;
      this.set$_lib_keys($.List(newCapacity));
      var t0 = $.List(newCapacity);
      $.setRuntimeTypeInfo(t0, ({E: 'V'}));
      this.set$_lib_values(t0);
      var i = 0;
      L0: while (true) {
        if (!$.ltB(i, capacity)) break L0;
        c$0:{
          var key = $.index(oldKeys, i);
          if (key === (void 0) || key === $.CTC2) {
            break c$0;
          }
          var value = $.index(oldValues, i);
          var newIndex = this._lib_probeForAdding$1(key);
          $.indexSet(this.get$_lib_keys(), newIndex, key);
          $.indexSet(this.get$_lib_values(), newIndex, value);
        }
        i = i + 1;
      }
      this.set$_lib_numberOfDeleted(0);
  }
 },
 _lib_ensureCapacity$0: function() {
  var newNumberOfEntries = $.add(this.get$_lib_numberOfEntries(), 1);
  if ($.geB(newNumberOfEntries, this.get$_lib_loadLimit())) {
    this._lib_grow$1($.mul($.get$length(this.get$_lib_keys()), 2));
    return;
  }
  var numberOfFree = $.sub($.sub($.get$length(this.get$_lib_keys()), newNumberOfEntries), this.get$_lib_numberOfDeleted());
  if ($.gtB(this.get$_lib_numberOfDeleted(), numberOfFree)) {
    this._lib_grow$1($.get$length(this.get$_lib_keys()));
  }
 },
 _lib_probeForLookup$1: function(key) {
  for (var hash = $._firstProbe($.hashCode(key), $.get$length(this.get$_lib_keys())), numberOfProbes = 1; true; ) {
    var existingKey = $.index(this.get$_lib_keys(), hash);
    if (existingKey === (void 0)) {
      return -1;
    }
    if ($.eqB(existingKey, key)) {
      return hash;
    }
    var numberOfProbes0 = numberOfProbes + 1;
    var hash0 = $._nextProbe(hash, numberOfProbes, $.get$length(this.get$_lib_keys()));
    numberOfProbes = numberOfProbes0;
    hash = hash0;
  }
 },
 _lib_probeForAdding$1: function(key) {
  var hash = $._firstProbe($.hashCode(key), $.get$length(this.get$_lib_keys()));
  if (hash !== (hash | 0)) return this._lib_probeForAdding$1$bailout(key, 1, hash);
  for (var numberOfProbes = 1, hash0 = hash, insertionIndex = -1; true; ) {
    var existingKey = $.index(this.get$_lib_keys(), hash0);
    if (existingKey === (void 0)) {
      if ($.ltB(insertionIndex, 0)) {
        return hash0;
      }
      return insertionIndex;
    } else {
      if ($.eqB(existingKey, key)) {
        return hash0;
      } else {
        if ($.ltB(insertionIndex, 0) && $.CTC2 === existingKey) {
          insertionIndex = hash0;
        }
        var numberOfProbes0 = numberOfProbes + 1;
      }
    }
    var hash1 = $._nextProbe(hash0, numberOfProbes, $.get$length(this.get$_lib_keys()));
    numberOfProbes = numberOfProbes0;
    hash0 = hash1;
  }
 },
 _lib_probeForAdding$1$bailout: function(key, state, env0) {
  switch (state) {
    case 1:
      hash = env0;
      break;
  }
  switch (state) {
    case 0:
      var hash = $._firstProbe($.hashCode(key), $.get$length(this.get$_lib_keys()));
    case 1:
      state = 0;
      var numberOfProbes = 1;
      var hash0 = hash;
      var insertionIndex = -1;
      L0: while (true) {
        if (!true) break L0;
        var existingKey = $.index(this.get$_lib_keys(), hash0);
        if (existingKey === (void 0)) {
          if ($.ltB(insertionIndex, 0)) {
            return hash0;
          }
          return insertionIndex;
        } else {
          if ($.eqB(existingKey, key)) {
            return hash0;
          } else {
            if ($.ltB(insertionIndex, 0) && $.CTC2 === existingKey) {
              insertionIndex = hash0;
            }
            var numberOfProbes0 = numberOfProbes + 1;
          }
        }
        var hash1 = $._nextProbe(hash0, numberOfProbes, $.get$length(this.get$_lib_keys()));
        numberOfProbes = numberOfProbes0;
        hash0 = hash1;
      }
  }
 },
 set$_lib_numberOfDeleted: function(v) { this._lib_numberOfDeleted = v; },
 get$_lib_numberOfDeleted: function() { return this._lib_numberOfDeleted; },
 set$_lib_numberOfEntries: function(v) { this._lib_numberOfEntries = v; },
 get$_lib_numberOfEntries: function() { return this._lib_numberOfEntries; },
 set$_lib_loadLimit: function(v) { this._lib_loadLimit = v; },
 get$_lib_loadLimit: function() { return this._lib_loadLimit; },
 set$_lib_values: function(v) { this._lib_values = v; },
 get$_lib_values: function() { return this._lib_values; },
 set$_lib_keys: function(v) { this._lib_keys = v; },
 get$_lib_keys: function() { return this._lib_keys; },
 HashMapImplementation$0: function() {
  this.set$_lib_numberOfEntries(0);
  this.set$_lib_numberOfDeleted(0);
  this.set$_lib_loadLimit($._computeLoadLimit(8));
  this.set$_lib_keys($.List(8));
  var t0 = $.List(8);
  $.setRuntimeTypeInfo(t0, ({E: 'V'}));
  this.set$_lib_values(t0);
 },
 is$Map: function() { return true; },
});

Isolate.$defineClass("_FileReaderEventsImpl", "_EventsImpl",
function _FileReaderEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("MVCNotifier", "Object",
function MVCNotifier() {
}, {
 set$multitonKey: function(v) { this.multitonKey = v; },
 get$multitonKey: function() { return this.multitonKey; },
 get$facade: function() {
  if ($.eqNullB(this.get$multitonKey())) {
    throw $.captureStackTrace($.NotifierLacksMultitonKeyError$0());
  }
  return $.getInstance(this.get$multitonKey());
 },
 initializeNotifier$1: function(key) {
  this.set$multitonKey(key);
 },
 sendNotification$3: function(noteName, body, type) {
  if (!$.eqNullB(this.get$facade())) {
    this.get$facade().sendNotification$3(noteName, body, type);
  }
 },
 sendNotification$1: function(noteName) {
  return this.sendNotification$3(noteName,(void 0),(void 0))
},
 sendNotification$2: function(noteName,body) {
  return this.sendNotification$3(noteName,body,(void 0))
},
 sendNotification$2: function(noteName,body) {
  return this.sendNotification$3(noteName,body,(void 0))
},
 MVCNotifier$0: function() {
 },
});

Isolate.$defineClass("_SharedWorkerContextEventsImpl", "_WorkerContextEventsImpl",
function _SharedWorkerContextEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_IDBVersionChangeRequestEventsImpl", "_IDBRequestEventsImpl",
function _IDBVersionChangeRequestEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("NoMoreElementsException", "Object",
function NoMoreElementsException() {
}, {
 toString$0: function() {
  return 'NoMoreElementsException';
 },
});

Isolate.$defineClass("Closure17", "Closure20",
function Closure(this_0) {
  this.this_0 = this_0;
}, {
 $call$1: function(value) {
  this.this_0.add$1(value);
 },
});

Isolate.$defineClass("_FrameSetElementEventsImpl", "_ElementEventsImpl",
function _FrameSetElementEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_FileWriterEventsImpl", "_EventsImpl",
function _FileWriterEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_FrozenElementList", "Object",
function _FrozenElementList(_lib3_nodeList) {
  this._lib3_nodeList = _lib3_nodeList;
}, {
 last$0: function() {
  return $.last(this.get$_lib3_nodeList());
 },
 removeLast$0: function() {
  throw $.captureStackTrace($.CTC4);
 },
 clear$0: function() {
  throw $.captureStackTrace($.CTC4);
 },
 indexOf$2: function(element, start) {
  return $.indexOf$2(this.get$_lib3_nodeList(), element, start);
 },
 getRange$2: function(start, rangeLength) {
  return $._lib3_FrozenElementList$_wrap$1($.getRange(this.get$_lib3_nodeList(), start, rangeLength));
 },
 addAll$1: function(collection) {
  throw $.captureStackTrace($.CTC4);
 },
 iterator$0: function() {
  return $._lib3_FrozenElementListIterator$1(this);
 },
 add$1: function(value) {
  throw $.captureStackTrace($.CTC4);
 },
 set$length: function(newLength) {
  $.set$length(this.get$_lib3_nodeList(), newLength);
 },
 operator$indexSet$2: function(index, value) {
  throw $.captureStackTrace($.CTC4);
 },
 operator$index$1: function(index) {
  return $.index(this.get$_lib3_nodeList(), index);
 },
 get$length: function() {
  return $.get$length(this.get$_lib3_nodeList());
 },
 isEmpty$0: function() {
  return $.isEmpty(this.get$_lib3_nodeList());
 },
 filter$1: function(f) {
  var out = $._lib3_ElementList$1([]);
  for (var t0 = this.iterator$0(); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    if (f.$call$1(t1) === true) {
      out.add$1(t1);
    }
  }
  return out;
 },
 forEach$1: function(f) {
  for (var t0 = this.iterator$0(); t0.hasNext$0() === true; ) {
    f.$call$1(t0.next$0());
  }
 },
 get$first: function() {
  return $.index(this.get$_lib3_nodeList(), 0);
 },
 first$0: function() { return this.get$first().$call$0(); },
 get$_lib3_nodeList: function() { return this._lib3_nodeList; },
 is$List2: function() { return true; },
 is$Collection: function() { return true; },
});

Isolate.$defineClass("NoSuchMethodException", "Object",
function NoSuchMethodException(_lib2_existingArgumentNames, _lib2_arguments, _lib2_functionName, _lib2_receiver) {
  this._lib2_existingArgumentNames = _lib2_existingArgumentNames;
  this._lib2_arguments = _lib2_arguments;
  this._lib2_functionName = _lib2_functionName;
  this._lib2_receiver = _lib2_receiver;
}, {
 get$_lib2_existingArgumentNames: function() { return this._lib2_existingArgumentNames; },
 get$_lib2_arguments: function() { return this._lib2_arguments; },
 get$_lib2_functionName: function() { return this._lib2_functionName; },
 get$_lib2_receiver: function() { return this._lib2_receiver; },
 toString$0: function() {
  var sb = $.StringBufferImpl$1('');
  for (var i = 0; $.ltB(i, $.get$length(this.get$_lib2_arguments())); i = i + 1) {
    if (i > 0) {
      sb.add$1(', ');
    }
    sb.add$1($.index(this.get$_lib2_arguments(), i));
  }
  if (this.get$_lib2_existingArgumentNames() === (void 0)) {
    return 'NoSuchMethodException : method not found: \'' + $.stringToString(this.get$_lib2_functionName()) + '\'\nReceiver: ' + $.stringToString(this.get$_lib2_receiver()) + '\nArguments: [' + $.stringToString(sb) + ']';
  } else {
    var actualParameters = sb.toString$0();
    var sb0 = $.StringBufferImpl$1('');
    for (var i0 = 0; $.ltB(i0, $.get$length(this.get$_lib2_existingArgumentNames())); i0 = i0 + 1) {
      if (i0 > 0) {
        sb0.add$1(', ');
      }
      sb0.add$1($.index(this.get$_lib2_existingArgumentNames(), i0));
    }
    var formalParameters = sb0.toString$0();
    return 'NoSuchMethodException: incorrect number of arguments passed to method named \'' + $.stringToString(this.get$_lib2_functionName()) + '\'\nReceiver: ' + $.stringToString(this.get$_lib2_receiver()) + '\nTried calling: ' + $.stringToString(this.get$_lib2_functionName()) + '(' + $.stringToString(actualParameters) + ')\nFound: ' + $.stringToString(this.get$_lib2_functionName()) + '(' + $.stringToString(formalParameters) + ')';
  }
 },
});

Isolate.$defineClass("_AbstractWorkerEventsImpl", "_EventsImpl",
function _AbstractWorkerEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("HashSetIterator", "Object",
function HashSetIterator(_lib_nextValidIndex, _lib_entries) {
  this._lib_nextValidIndex = _lib_nextValidIndex;
  this._lib_entries = _lib_entries;
}, {
 set$_lib_nextValidIndex: function(v) { this._lib_nextValidIndex = v; },
 get$_lib_nextValidIndex: function() { return this._lib_nextValidIndex; },
 get$_lib_entries: function() { return this._lib_entries; },
 _lib_advance$0: function() {
  var length$ = $.get$length(this.get$_lib_entries());
  if (typeof length$ !== 'number') return this._lib_advance$0$bailout(1, length$);
  var entry = (void 0);
  do {
    var t0 = $.add(this.get$_lib_nextValidIndex(), 1);
    this.set$_lib_nextValidIndex(t0);
    if ($.geB(t0, length$)) {
      break;
    }
    entry = $.index(this.get$_lib_entries(), this.get$_lib_nextValidIndex());
  } while (entry === (void 0) || entry === $.CTC2);
 },
 _lib_advance$0$bailout: function(state, env0) {
  switch (state) {
    case 1:
      length$ = env0;
      break;
  }
  switch (state) {
    case 0:
      var length$ = $.get$length(this.get$_lib_entries());
    case 1:
      state = 0;
      var entry = (void 0);
      L0: while (true) {
        var t0 = $.add(this.get$_lib_nextValidIndex(), 1);
        this.set$_lib_nextValidIndex(t0);
        if ($.geB(t0, length$)) {
          break;
        }
        entry = $.index(this.get$_lib_entries(), this.get$_lib_nextValidIndex());
        if (!(entry === (void 0) || entry === $.CTC2)) break L0;
      }
  }
 },
 next$0: function() {
  if (!(this.hasNext$0() === true)) {
    throw $.captureStackTrace($.CTC3);
  }
  var res = $.index(this.get$_lib_entries(), this.get$_lib_nextValidIndex());
  this._lib_advance$0();
  return res;
 },
 hasNext$0: function() {
  if ($.geB(this.get$_lib_nextValidIndex(), $.get$length(this.get$_lib_entries()))) {
    return false;
  }
  if ($.index(this.get$_lib_entries(), this.get$_lib_nextValidIndex()) === $.CTC2) {
    this._lib_advance$0();
  }
  return $.lt(this.get$_lib_nextValidIndex(), $.get$length(this.get$_lib_entries()));
 },
 HashSetIterator$1: function(set_) {
  this._lib_advance$0();
 },
});

Isolate.$defineClass("IllegalArgumentException", "Object",
function IllegalArgumentException(_lib2_arg) {
  this._lib2_arg = _lib2_arg;
}, {
 get$_lib2_arg: function() { return this._lib2_arg; },
 toString$0: function() {
  return 'Illegal argument(s): ' + $.stringToString(this.get$_lib2_arg());
 },
});

Isolate.$defineClass("_MediaElementEventsImpl", "_ElementEventsImpl",
function _MediaElementEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_IDBTransactionEventsImpl", "_EventsImpl",
function _IDBTransactionEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_BodyElementEventsImpl", "_ElementEventsImpl",
function _BodyElementEventsImpl(_EventsImpl__lib3_ptr) {
  this._lib3_ptr = _EventsImpl__lib3_ptr;
}, {
});

Isolate.$defineClass("_AllMatchesIterator", "Object",
function _AllMatchesIterator(_lib_done, _lib_next, _lib_str, _lib_re) {
  this._lib_done = _lib_done;
  this._lib_next = _lib_next;
  this._lib_str = _lib_str;
  this._lib_re = _lib_re;
}, {
 hasNext$0: function() {
  if (this.get$_lib_done() === true) {
    return false;
  } else {
    if (!$.eqNullB(this.get$_lib_next())) {
      return true;
    }
  }
  this.set$_lib_next(this.get$_lib_re().firstMatch$1(this.get$_lib_str()));
  if ($.eqNullB(this.get$_lib_next())) {
    this.set$_lib_done(true);
    return false;
  } else {
    return true;
  }
 },
 next$0: function() {
  if (!(this.hasNext$0() === true)) {
    throw $.captureStackTrace($.CTC3);
  }
  var next = this.get$_lib_next();
  this.set$_lib_next((void 0));
  return next;
 },
 set$_lib_done: function(v) { this._lib_done = v; },
 get$_lib_done: function() { return this._lib_done; },
 set$_lib_next: function(v) { this._lib_next = v; },
 get$_lib_next: function() { return this._lib_next; },
 get$_lib_str: function() { return this._lib_str; },
 get$_lib_re: function() { return this._lib_re; },
});

Isolate.$defineClass("Closure20", "Object",
function Closure() {
}, {
 toString$0: function() {
  return 'Closure';
 },
});

Isolate.$defineClass('Closure21', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$1: function(arg0) {
  return this.self.add$1(arg0);
},
});
Isolate.$defineClass('Closure22', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$1: function(arg0) {
  return this.self.handleNotification$1(arg0);
},
});
Isolate.$defineClass('Closure23', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$0: function() {
  return this.self.click$0();
},
});
Isolate.$defineClass('Closure24', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$0: function() {
  return this.self.click$0();
},
});
Isolate.$defineClass('Closure25', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$1: function(arg0) {
  return this.self.handleNotification$1(arg0);
},
});
Isolate.$defineClass('Closure26', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$1: function(arg0) {
  return this.self.handleEvent$1(arg0);
},
});
Isolate.$defineClass('Closure27', 'Closure20', function BoundClosure(self) { this.self = self; }, {
$call$1: function(arg0) {
  return this.self.executeCommand$1(arg0);
},
});
$._lib3_ChildNodeListLazy$1 = function(_this) {
  return new $._ChildNodeListLazy(_this);
};

$._lib3_AudioContextEventsImpl$1 = function(_ptr) {
  return new $._AudioContextEventsImpl(_ptr);
};

$.floor = function(receiver) {
  if (!(typeof receiver === 'number')) {
    return receiver.floor$0();
  }
  return Math.floor(receiver);
};

$.eqB = function(a, b) {
  return $.eq(a, b) === true;
};

$._containsRef = function(c, ref) {
  for (var t0 = $.iterator(c); t0.hasNext$0() === true; ) {
    if (t0.next$0() === ref) {
      return true;
    }
  }
  return false;
};

$._lib3_NodeListWrapper$1 = function(list) {
  return new $._NodeListWrapper(list);
};

$.isJsArray = function(value) {
  return !(value === (void 0)) && (value.constructor === Array);
};

$._nextProbe = function(currentProbe, numberOfProbes, length$) {
  return $.and($.add(currentProbe, numberOfProbes), $.sub(length$, 1));
};

$.allMatches = function(receiver, str) {
  if (!(typeof receiver === 'string')) {
    return receiver.allMatches$1(str);
  }
  $.checkString(str);
  return $.allMatchesInStringUnchecked(receiver, str);
};

$.substringUnchecked = function(receiver, startIndex, endIndex) {
  return receiver.substring(startIndex, endIndex);
};

$.StartupCommand$0 = function() {
  var t0 = new $.StartupCommand((void 0), (void 0));
  t0.MVCNotifier$0();
  t0.MVCMacroCommand$0();
  return t0;
};

$.get$length = function(receiver) {
  if (typeof receiver === 'string' || $.isJsArray(receiver) === true) {
    return receiver.length;
  } else {
    return receiver.get$length();
  }
};

$.TextComponent$0 = function() {
  var t0 = new $.TextComponent((void 0), (void 0), (void 0), (void 0), (void 0), (void 0));
  t0.TextComponent$0();
  return t0;
};

$.IllegalJSRegExpException$2 = function(_pattern, _errmsg) {
  return new $.IllegalJSRegExpException(_errmsg, _pattern);
};

$.ProcessTextCommand$0 = function() {
  var t0 = new $.ProcessTextCommand((void 0));
  t0.MVCNotifier$0();
  return t0;
};

$.typeNameInIE = function(obj) {
  var name$ = $.constructorNameFallback(obj);
  if ($.eqB(name$, 'Window')) {
    return 'DOMWindow';
  }
  if ($.eqB(name$, 'Document')) {
    if (!!obj.xmlVersion) {
      return 'Document';
    }
    return 'HTMLDocument';
  }
  if ($.eqB(name$, 'HTMLTableDataCellElement')) {
    return 'HTMLTableCellElement';
  }
  if ($.eqB(name$, 'HTMLTableHeaderCellElement')) {
    return 'HTMLTableCellElement';
  }
  if ($.eqB(name$, 'MSStyleCSSProperties')) {
    return 'CSSStyleDeclaration';
  }
  return name$;
};

$.regExpMatchStart = function(m) {
  return m.index;
};

$.MultitonViewExistsError$0 = function() {
  return new $.MultitonViewExistsError();
};

$.constructorNameFallback = function(obj) {
  var constructor$ = (obj.constructor);
  if ((typeof(constructor$)) === 'function') {
    var name$ = (constructor$.name);
    if ((typeof(name$)) === 'string' && !($.isEmpty(name$) === true) && !(name$ === 'Object')) {
      return name$;
    }
  }
  var string = (Object.prototype.toString.call(obj));
  return $.substring$2(string, 8, string.length - 1);
};

$.NullPointerException$2 = function(functionName, arguments$) {
  return new $.NullPointerException(arguments$, functionName);
};

$.tdiv = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return $.truncate($.div(a, b));
  }
  return a.operator$tdiv$1(b);
};

$.printString = function(string) {
  if (typeof console == "object") {
    console.log(string);
  } else {
    write(string);
    write("\n");
  }
};

$.JSSyntaxRegExp$_globalVersionOf$1 = function(other) {
  var t0 = other.get$pattern();
  var t1 = other.get$multiLine();
  var t2 = new $.JSSyntaxRegExp(other.get$ignoreCase(), t1, t0);
  t2.JSSyntaxRegExp$_globalVersionOf$1(other);
  return t2;
};

$.typeNameInChrome = function(obj) {
  var name$ = (obj.constructor.name);
  if (name$ === 'Window') {
    return 'DOMWindow';
  }
  if (name$ === 'CanvasPixelArray') {
    return 'Uint8ClampedArray';
  }
  return name$;
};

$.clear = function(receiver) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.clear$0();
  }
  $.set$length(receiver, 0);
};

$.shr = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    if ($.ltB(b, 0)) {
      throw $.captureStackTrace($.IllegalArgumentException$1(b));
    }
    return a >> b;
  }
  return a.operator$shr$1(b);
};

$.eqNull = function(a) {
  if (typeof a === "object") {
    if (!!a.operator$eq$1) {
      return a.operator$eq$1((void 0));
    } else {
      return false;
    }
  } else {
    return typeof a === "undefined";
  }
};

$.and = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a & b;
  }
  return a.operator$and$1(b);
};

$.substring$2 = function(receiver, startIndex, endIndex) {
  if (!(typeof receiver === 'string')) {
    return receiver.substring$2(startIndex, endIndex);
  }
  $.checkNum(startIndex);
  var length$ = receiver.length;
  var endIndex0 = endIndex;
  if (endIndex === (void 0)) {
    endIndex0 = length$;
  }
  $.checkNum(endIndex0);
  if ($.ltB(startIndex, 0)) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(startIndex));
  }
  if ($.gtB(startIndex, endIndex0)) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(startIndex));
  }
  if ($.gtB(endIndex0, length$)) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(endIndex0));
  }
  return $.substringUnchecked(receiver, startIndex, endIndex0);
};

$.indexSet = function(a, index, value) {
  if ($.isJsArray(a) === true) {
    if (!((typeof index === 'number') && (index === (index | 0)))) {
      throw $.captureStackTrace($.IllegalArgumentException$1(index));
    }
    if (index < 0 || $.geB(index, $.get$length(a))) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(index));
    }
    $.checkMutable(a, 'indexed set');
    a[index] = value;
    return;
  }
  a.operator$indexSet$2(index, value);
};

$._lib3_DOMApplicationCacheEventsImpl$1 = function(_ptr) {
  return new $._DOMApplicationCacheEventsImpl(_ptr);
};

$.ExceptionImplementation$1 = function(msg) {
  return new $.ExceptionImplementation(msg);
};

$.StringMatch$3 = function(_start, str, pattern) {
  return new $.StringMatch(pattern, str, _start);
};

$.invokeClosure = function(closure, isolate, numberOfArguments, arg1, arg2) {
  var t0 = ({});
  t0.arg2_3 = arg2;
  t0.arg1_2 = arg1;
  t0.closure_1 = closure;
  if ($.eqB(numberOfArguments, 0)) {
    return new $.Closure6(t0).$call$0();
  } else {
    if ($.eqB(numberOfArguments, 1)) {
      return new $.Closure7(t0).$call$0();
    } else {
      if ($.eqB(numberOfArguments, 2)) {
        return new $.Closure8(t0).$call$0();
      } else {
        throw $.captureStackTrace($.ExceptionImplementation$1('Unsupported number of arguments for wrapped closure'));
      }
    }
  }
};

$.last = function(receiver) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.last$0();
  }
  return $.index(receiver, $.sub($.get$length(receiver), 1));
};

$.gt = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a > b;
  }
  return a.operator$gt$1(b);
};

$.assert = function(condition) {
};

$.filter = function(receiver, predicate) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.filter$1(predicate);
  } else {
    return $.filter2(receiver, [], predicate);
  }
};

$.filter2 = function(source, destination, f) {
  for (var t0 = $.iterator(source); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    if (f.$call$1(t1) === true) {
      $.add$1(destination, t1);
    }
  }
  return destination;
};

$.buildDynamicMetadata = function(inputTable) {
  if (typeof inputTable !== 'string' && (typeof inputTable !== 'object'||inputTable.constructor !== Array)) return $.buildDynamicMetadata$bailout(inputTable,  0);
  var result = [];
  for (var i = 0; i < inputTable.length; i = i + 1) {
    var t0 = inputTable.length;
    if (i < 0 || i >= t0) throw $.ioore(i);
    var tag = $.index(inputTable[i], 0);
    var t1 = inputTable.length;
    if (i < 0 || i >= t1) throw $.ioore(i);
    var tags = $.index(inputTable[i], 1);
    var set = $.HashSetImplementation$0();
    $.setRuntimeTypeInfo(set, ({E: 'String'}));
    var tagNames = $.split(tags, '|');
    if (typeof tagNames !== 'string' && (typeof tagNames !== 'object'||tagNames.constructor !== Array)) return $.buildDynamicMetadata$bailout(inputTable, 2, inputTable, result, tag, i, tags, set, tagNames);
    for (var j = 0; j < tagNames.length; j = j + 1) {
      var t2 = tagNames.length;
      if (j < 0 || j >= t2) throw $.ioore(j);
      set.add$1(tagNames[j]);
    }
    $.add$1(result, $.MetaInfo$3(tag, tags, set));
  }
  return result;
};

$.filter3 = function(source, destination, f) {
  for (var t0 = $.iterator(source); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    if (f.$call$1(t1) === true) {
      $.add$1(destination, t1);
    }
  }
  return destination;
};

$.contains$1 = function(receiver, other) {
  if (!(typeof receiver === 'string')) {
    return receiver.contains$1(other);
  }
  return $.contains$2(receiver, other, 0);
};

$._lib3_EventSourceEventsImpl$1 = function(_ptr) {
  return new $._EventSourceEventsImpl(_ptr);
};

$.mul = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a * b;
  }
  return a.operator$mul$1(b);
};

$._lib3_NotificationEventsImpl$1 = function(_ptr) {
  return new $._NotificationEventsImpl(_ptr);
};

$._browserPrefix = function() {
  if ($._cachedBrowserPrefix === (void 0)) {
    if ($.isFirefox() === true) {
      $._cachedBrowserPrefix = '-moz-';
    } else {
      $._cachedBrowserPrefix = '-webkit-';
    }
  }
  return $._cachedBrowserPrefix;
};

$._emitCollection = function(c, result, visiting) {
  $.add$1(visiting, c);
  var isList = typeof c === 'object' && (c.constructor === Array || c.is$List2());
  if (isList) {
    var t0 = '[';
  } else {
    t0 = '{';
  }
  $.add$1(result, t0);
  for (var t1 = $.iterator(c), first = true; t1.hasNext$0() === true; ) {
    var t2 = t1.next$0();
    if (!first) {
      $.add$1(result, ', ');
    }
    $._emitObject(t2, result, visiting);
    first = false;
  }
  if (isList) {
    var t3 = ']';
  } else {
    t3 = '}';
  }
  $.add$1(result, t3);
  $.removeLast(visiting);
};

$.checkMutable = function(list, reason) {
  if (!!(list.immutable$list)) {
    throw $.captureStackTrace($.UnsupportedOperationException$1(reason));
  }
};

$.PrepareControllerCommand$0 = function() {
  var t0 = new $.PrepareControllerCommand((void 0));
  t0.MVCNotifier$0();
  return t0;
};

$.toStringWrapper = function() {
  return $.toString((this.dartException));
};

$._lib3_PeerConnection00EventsImpl$1 = function(_ptr) {
  return new $._PeerConnection00EventsImpl(_ptr);
};

$._lib3_ElementList$1 = function(list) {
  return new $._ElementList(list);
};

$.MVCFacade$1 = function(key) {
  var t0 = new $.MVCFacade((void 0), (void 0), (void 0), (void 0));
  t0.MVCFacade$1(key);
  return t0;
};

$._lib3_WorkerContextEventsImpl$1 = function(_ptr) {
  return new $._WorkerContextEventsImpl(_ptr);
};

$._lib3_DocumentEventsImpl$1 = function(_ptr) {
  return new $._DocumentEventsImpl(_ptr);
};

$.regExpTest = function(regExp, str) {
  return $.regExpGetNative(regExp).test(str);
};

$.isEmpty = function(receiver) {
  if (typeof receiver === 'string' || $.isJsArray(receiver) === true) {
    return receiver.length === 0;
  }
  return receiver.isEmpty$0();
};

$._lib3_EventsImpl$1 = function(_ptr) {
  return new $._EventsImpl(_ptr);
};

$.HashSetImplementation$0 = function() {
  var t0 = new $.HashSetImplementation((void 0));
  t0.HashSetImplementation$0();
  return t0;
};

$._lib3_IDBRequestEventsImpl$1 = function(_ptr) {
  return new $._IDBRequestEventsImpl(_ptr);
};

$.stringSplitUnchecked = function(receiver, pattern) {
  if (typeof pattern === 'string') {
    return receiver.split(pattern);
  } else {
    if (typeof pattern === 'object' && !!pattern.is$JSSyntaxRegExp) {
      return receiver.split($.regExpGetNative(pattern));
    } else {
      throw $.captureStackTrace('StringImplementation.split(Pattern) UNIMPLEMENTED');
    }
  }
};

$.checkGrowable = function(list, reason) {
  if (!!(list.fixed$length)) {
    throw $.captureStackTrace($.UnsupportedOperationException$1(reason));
  }
};

$.MVCNotification$3 = function(name$, body, type) {
  var t0 = new $.MVCNotification(body, type, name$);
  t0.MVCNotification$3(name$, body, type);
  return t0;
};

$._lib3_SpeechRecognitionEventsImpl$1 = function(_ptr) {
  return new $._SpeechRecognitionEventsImpl(_ptr);
};

$._lib3_SVGElementInstanceEventsImpl$1 = function(_ptr) {
  return new $._SVGElementInstanceEventsImpl(_ptr);
};

$.add$1 = function(receiver, value) {
  if ($.isJsArray(receiver) === true) {
    $.checkGrowable(receiver, 'add');
    receiver.push(value);
    return;
  }
  return receiver.add$1(value);
};

$.regExpExec = function(regExp, str) {
  var result = ($.regExpGetNative(regExp).exec(str));
  if (result === null) {
    return;
  }
  return result;
};

$.geB = function(a, b) {
  return $.ge(a, b) === true;
};

$.NotifierLacksMultitonKeyError$0 = function() {
  return new $.NotifierLacksMultitonKeyError();
};

$.stringContainsUnchecked = function(receiver, other, startIndex) {
  if (typeof other === 'string') {
    return !($.indexOf$2(receiver, other, startIndex) === -1);
  } else {
    if (typeof other === 'object' && !!other.is$JSSyntaxRegExp) {
      return other.hasMatch$1($.substring$1(receiver, startIndex));
    } else {
      return $.iterator($.allMatches(other, $.substring$1(receiver, startIndex))).hasNext$0();
    }
  }
};

$.PrepareModelCommand$0 = function() {
  var t0 = new $.PrepareModelCommand((void 0));
  t0.MVCNotifier$0();
  return t0;
};

$.ObjectNotClosureException$0 = function() {
  return new $.ObjectNotClosureException();
};

$.iterator = function(receiver) {
  if ($.isJsArray(receiver) === true) {
    return $.ListIterator$1(receiver);
  }
  return receiver.iterator$0();
};

$.window = function() {
  return window;;
};

$.add = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a + b;
  } else {
    if (typeof a === 'string') {
      var b0 = $.toString(b);
      if (typeof b0 === 'string') {
        return a + b0;
      }
      $.checkNull(b0);
      throw $.captureStackTrace($.IllegalArgumentException$1(b0));
    }
  }
  return a.operator$add$1(b);
};

$.regExpAttachGlobalNative = function(regExp) {
  regExp._re = $.regExpMakeNative(regExp, true);
};

$.regExpMakeNative = function(regExp, global) {
  var pattern = regExp.get$pattern();
  var multiLine = regExp.get$multiLine();
  var ignoreCase = regExp.get$ignoreCase();
  $.checkString(pattern);
  var sb = $.StringBufferImpl$1('');
  if (multiLine === true) {
    $.add$1(sb, 'm');
  }
  if (ignoreCase === true) {
    $.add$1(sb, 'i');
  }
  if (global === true) {
    $.add$1(sb, 'g');
  }
  try {
    return new RegExp(pattern, $.toString(sb));
}  catch (t0) {
    var t1 = $.unwrapException(t0);
    var e = t1;
    throw $.captureStackTrace($.IllegalJSRegExpException$2(pattern, (String(e))));
  }
};

$.splitChars = function(receiver) {
  if (!(typeof receiver === 'string')) {
    return receiver.splitChars$0();
  }
  return receiver.split("");
};

$._lib3_FrozenElementListIterator$1 = function(_list) {
  return new $._FrozenElementListIterator(0, _list);
};

$.mapToString = function(m) {
  var result = $.StringBufferImpl$1('');
  $._emitMap(m, result, $.List((void 0)));
  return result.toString$0();
};

$.TextComponentMediator$1 = function(viewComponent) {
  var t0 = $.NAME;
  var t1 = new $.TextComponentMediator(viewComponent, t0, (void 0));
  t1.MVCNotifier$0();
  t1.MVCMediator$2(t0, viewComponent);
  t1.TextComponentMediator$1(viewComponent);
  return t1;
};

$._lib3_XMLHttpRequestEventsImpl$1 = function(_ptr) {
  return new $._XMLHttpRequestEventsImpl(_ptr);
};

$._lib3_JavaScriptAudioNodeEventsImpl$1 = function(_ptr) {
  return new $._JavaScriptAudioNodeEventsImpl(_ptr);
};

$._emitObject = function(o, result, visiting) {
  if (typeof o === 'object' && (o.constructor === Array || o.is$Collection())) {
    if ($._containsRef(visiting, o) === true) {
      if (typeof o === 'object' && (o.constructor === Array || o.is$List2())) {
        var t0 = '[...]';
      } else {
        t0 = '{...}';
      }
      $.add$1(result, t0);
    } else {
      $._emitCollection(o, result, visiting);
    }
  } else {
    if (typeof o === 'object' && o.is$Map()) {
      if ($._containsRef(visiting, o) === true) {
        $.add$1(result, '{...}');
      } else {
        $._emitMap(o, result, visiting);
      }
    } else {
      if ($.eqNullB(o)) {
        var t1 = 'null';
      } else {
        t1 = o;
      }
      $.add$1(result, t1);
    }
  }
};

$._emitMap = function(m, result, visiting) {
  var t0 = ({});
  t0.visiting_2 = visiting;
  t0.result_1 = result;
  $.add$1(t0.visiting_2, m);
  $.add$1(t0.result_1, '{');
  t0.first_3 = true;
  $.forEach(m, new $.Closure2(t0));
  $.add$1(t0.result_1, '}');
  $.removeLast(t0.visiting_2);
};

$._lib3_IDBDatabaseEventsImpl$1 = function(_ptr) {
  return new $._IDBDatabaseEventsImpl(_ptr);
};

$.isFirefox = function() {
  return $.contains$2($.userAgent(), 'Firefox', 0);
};

$.ge = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a >= b;
  }
  return a.operator$ge$1(b);
};

$._lib3_TextTrackCueEventsImpl$1 = function(_ptr) {
  return new $._TextTrackCueEventsImpl(_ptr);
};

$.MatchImplementation$5 = function(pattern, str, _start, _end, _groups) {
  return new $.MatchImplementation(_groups, _end, _start, str, pattern);
};

$.UnsupportedOperationException$1 = function(_message) {
  return new $.UnsupportedOperationException(_message);
};

$.MVCController$1 = function(key) {
  var t0 = new $.MVCController((void 0), (void 0), (void 0));
  t0.MVCController$1(key);
  return t0;
};

$.indexOf$2 = function(receiver, element, start) {
  if ($.isJsArray(receiver) === true) {
    if (!((typeof start === 'number') && (start === (start | 0)))) {
      throw $.captureStackTrace($.IllegalArgumentException$1(start));
    }
    return $.indexOf(receiver, element, start, (receiver.length));
  } else {
    if (typeof receiver === 'string') {
      $.checkNull(element);
      if (!((typeof start === 'number') && (start === (start | 0)))) {
        throw $.captureStackTrace($.IllegalArgumentException$1(start));
      }
      if (!(typeof element === 'string')) {
        throw $.captureStackTrace($.IllegalArgumentException$1(element));
      }
      if (start < 0) {
        return -1;
      }
      return receiver.indexOf(element, start);
    }
  }
  return receiver.indexOf$2(element, start);
};

$._lib3_DedicatedWorkerContextEventsImpl$1 = function(_ptr) {
  return new $._DedicatedWorkerContextEventsImpl(_ptr);
};

$._lib3_FileReaderEventsImpl$1 = function(_ptr) {
  return new $._FileReaderEventsImpl(_ptr);
};

$.NoMoreElementsException$0 = function() {
  return new $.NoMoreElementsException();
};

$.eqNullB = function(a) {
  return $.eqNull(a) === true;
};

$.Element$tag = function(tag) {
  return document.createElement(tag);
};

$._lib3_FrameSetElementEventsImpl$1 = function(_ptr) {
  return new $._FrameSetElementEventsImpl(_ptr);
};

$.List$from = function(other) {
  var result = $.List((void 0));
  $.setRuntimeTypeInfo(result, ({E: 'E'}));
  var iterator = $.iterator(other);
  for (; iterator.hasNext$0() === true; ) {
    result.push(iterator.next$0());
  }
  return result;
};

$.newList = function(length$) {
  if (length$ === (void 0)) {
    return new Array();
  }
  var t0 = typeof length$ === 'number' && length$ === (length$ | 0);
  var t1 = !t0;
  if (t0) {
    t1 = length$ < 0;
  }
  if (t1) {
    throw $.captureStackTrace($.IllegalArgumentException$1(length$));
  }
  var result = (new Array(length$));
  result.fixed$length = true;
  return result;
};

$.main = function() {
  $.print('2');
  var facade = $.getInstance('ReverseText');
  facade.registerCommand$2('startup', new $.Closure());
  facade.sendNotification$1('startup');
};

$._lib3_AbstractWorkerEventsImpl$1 = function(_ptr) {
  return new $._AbstractWorkerEventsImpl(_ptr);
};

$._computeLoadLimit = function(capacity) {
  return $.tdiv($.mul(capacity, 3), 4);
};

$.HashSetIterator$1 = function(set_) {
  var t0 = new $.HashSetIterator(-1, set_.get$_lib_backingMap().get$_lib_keys());
  t0.HashSetIterator$1(set_);
  return t0;
};

$.IllegalArgumentException$1 = function(arg) {
  return new $.IllegalArgumentException(arg);
};

$._lib3_MediaElementEventsImpl$1 = function(_ptr) {
  return new $._MediaElementEventsImpl(_ptr);
};

$._lib3_IDBTransactionEventsImpl$1 = function(_ptr) {
  return new $._IDBTransactionEventsImpl(_ptr);
};

$._lib3_BodyElementEventsImpl$1 = function(_ptr) {
  return new $._BodyElementEventsImpl(_ptr);
};

$._lib_AllMatchesIterator$2 = function(re, _str) {
  return new $._AllMatchesIterator(false, (void 0), _str, $.JSSyntaxRegExp$_globalVersionOf$1(re));
};

$.iae = function(argument) {
  throw $.captureStackTrace($.IllegalArgumentException$1(argument));
};

$.truncate = function(receiver) {
  if (!(typeof receiver === 'number')) {
    return receiver.truncate$0();
  }
  if (receiver < 0) {
    var t0 = $.ceil(receiver);
  } else {
    t0 = $.floor(receiver);
  }
  return t0;
};

$.MVCObserver$2 = function(notifyMethod, notifyContext) {
  var t0 = new $.MVCObserver(notifyContext, notifyMethod);
  t0.MVCObserver$2(notifyMethod, notifyContext);
  return t0;
};

$.MultitonModelExistsError$0 = function() {
  return new $.MultitonModelExistsError();
};

$.PrepareViewCommand$0 = function() {
  var t0 = new $.PrepareViewCommand((void 0));
  t0.MVCNotifier$0();
  return t0;
};

$.allMatchesInStringUnchecked = function(needle, haystack) {
  var result = $.List((void 0));
  $.setRuntimeTypeInfo(result, ({E: 'Match'}));
  var length$ = $.get$length(haystack);
  var patternLength = $.get$length(needle);
  if (patternLength !== (patternLength | 0)) return $.allMatchesInStringUnchecked$bailout(needle, haystack, 1, length$, result, patternLength);
  for (var startIndex = 0; true; ) {
    var position = $.indexOf$2(haystack, needle, startIndex);
    if ($.eqB(position, -1)) {
      break;
    }
    result.push($.StringMatch$3(position, haystack, needle));
    var endIndex = $.add(position, patternLength);
    if ($.eqB(endIndex, length$)) {
      break;
    } else {
      if ($.eqB(position, endIndex)) {
        startIndex = $.add(startIndex, 1);
      } else {
        startIndex = endIndex;
      }
    }
  }
  return result;
};

$.MultitonFacadeExistsError$0 = function() {
  return new $.MultitonFacadeExistsError();
};

$._lib3_ChildrenElementList$_wrap$1 = function(element) {
  return new $._ChildrenElementList(element.get$$dom_children(), element);
};

$._lib_AllMatchesIterable$2 = function(_re, _str) {
  return new $._AllMatchesIterable(_str, _re);
};

$.dynamicSetMetadata = function(inputTable) {
  var t0 = $.buildDynamicMetadata(inputTable);
  $._dynamicMetadata(t0);
};

$.ListIterator$1 = function(list) {
  return new $.ListIterator(list, 0);
};

$.checkNum = function(value) {
  if (!(typeof value === 'number')) {
    $.checkNull(value);
    throw $.captureStackTrace($.IllegalArgumentException$1(value));
  }
  return value;
};

$._lib3_WorkerEventsImpl$1 = function(_ptr) {
  return new $._WorkerEventsImpl(_ptr);
};

$.ltB = function(a, b) {
  return $.lt(a, b) === true;
};

$.FilteredElementList$1 = function(node) {
  return new $.FilteredElementList(node.get$nodes(), node);
};

$.convertDartClosureToJS = function(closure) {
  if (closure === (void 0)) {
    return;
  }
  var function$ = (closure.$identity);
  if (!!function$) {
    return function$;
  }
  var function0 = (function() {
    return $.invokeClosure.$call$5(closure, $, arguments.length, arguments[0], arguments[1]);
  });
  closure.$identity = function0;
  return function0;
};

$._lib3_FixedSizeListIterator$1 = function(array) {
  return new $._FixedSizeListIterator($.get$length(array), 0, array);
};

$._lib3_FrozenElementList$_wrap$1 = function(_nodeList) {
  return new $._FrozenElementList(_nodeList);
};

$.split = function(receiver, pattern) {
  if (!(typeof receiver === 'string')) {
    return receiver.split$1(pattern);
  }
  $.checkNull(pattern);
  return $.stringSplitUnchecked(receiver, pattern);
};

$.concatAll = function(strings) {
  $.checkNull(strings);
  for (var t0 = $.iterator(strings), result = ''; t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    $.checkNull(t1);
    if (!(typeof t1 === 'string')) {
      throw $.captureStackTrace($.IllegalArgumentException$1(t1));
    }
    result = result + t1;
  }
  return result;
};

$.userAgent = function() {
  return $.window().get$navigator().get$userAgent();
};

$._lib3_InputElementEventsImpl$1 = function(_ptr) {
  return new $._InputElementEventsImpl(_ptr);
};

$.getRange = function(receiver, start, length$) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.getRange$2(start, length$);
  }
  if (0 === length$) {
    return [];
  }
  $.checkNull(start);
  $.checkNull(length$);
  if (!((typeof start === 'number') && (start === (start | 0)))) {
    throw $.captureStackTrace($.IllegalArgumentException$1(start));
  }
  if (!((typeof length$ === 'number') && (length$ === (length$ | 0)))) {
    throw $.captureStackTrace($.IllegalArgumentException$1(length$));
  }
  if (length$ < 0) {
    throw $.captureStackTrace($.IllegalArgumentException$1(length$));
  }
  if (start < 0) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(start));
  }
  var end = start + length$;
  if ($.gtB(end, $.get$length(receiver))) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(length$));
  }
  if ($.ltB(length$, 0)) {
    throw $.captureStackTrace($.IllegalArgumentException$1(length$));
  }
  return receiver.slice(start, end);
};

$.getRange2 = function(a, start, length$, accumulator) {
  if (typeof a !== 'string' && (typeof a !== 'object'||a.constructor !== Array)) return $.getRange2$bailout(a, start, length$, accumulator,  0);
  if (typeof start !== 'number') return $.getRange2$bailout(a, start, length$, accumulator,  0);
  if ($.ltB(length$, 0)) {
    throw $.captureStackTrace($.IllegalArgumentException$1('length'));
  }
  if (start < 0) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(start));
  }
  var end = $.add(start, length$);
  if (end > a.length) {
    throw $.captureStackTrace($.IndexOutOfRangeException$1(end));
  }
  for (var i = start; i < end; i = i + 1) {
    if (i !== (i | 0)) throw $.iae(i);
    var t0 = a.length;
    if (i < 0 || i >= t0) throw $.ioore(i);
    $.add$1(accumulator, a[i]);
  }
  return accumulator;
};

$._lib3_TextTrackListEventsImpl$1 = function(_ptr) {
  return new $._TextTrackListEventsImpl(_ptr);
};

$._dynamicMetadata = function(table) {
  $dynamicMetadata = table;
};

$._dynamicMetadata2 = function() {
  if ((typeof($dynamicMetadata)) === 'undefined') {
    var t0 = [];
    $._dynamicMetadata(t0);
  }
  return $dynamicMetadata;
};

$._lib3_DeprecatedPeerConnectionEventsImpl$1 = function(_ptr) {
  return new $._DeprecatedPeerConnectionEventsImpl(_ptr);
};

$.regExpGetNative = function(regExp) {
  var r = (regExp._re);
  var r0 = r;
  if (r === (void 0)) {
    r0 = (regExp._re = $.regExpMakeNative(regExp, false));
  }
  return r0;
};

$.checkNull = function(object) {
  if (object === (void 0)) {
    throw $.captureStackTrace($.NullPointerException$2((void 0), $.CTC));
  }
  return object;
};

$.throwNoSuchMethod = function(obj, name$, arguments$) {
  throw $.captureStackTrace($.NoSuchMethodException$4(obj, name$, arguments$, (void 0)));
};

$._lib3_EventListenerListImpl$2 = function(_ptr, _type) {
  return new $._EventListenerListImpl(_type, _ptr);
};

$.MVCModel$1 = function(key) {
  var t0 = new $.MVCModel((void 0), (void 0));
  t0.MVCModel$1(key);
  return t0;
};

$._lib3_WindowEventsImpl$1 = function(_ptr) {
  return new $._WindowEventsImpl(_ptr);
};

$.checkNumbers = function(a, b) {
  if (typeof a === 'number') {
    if (typeof b === 'number') {
      return true;
    } else {
      $.checkNull(b);
      throw $.captureStackTrace($.IllegalArgumentException$1(b));
    }
  }
  return false;
};

$.stringToString = function(value) {
  var res = $.toString(value);
  if (!(typeof res === 'string')) {
    throw $.captureStackTrace($.IllegalArgumentException$1(value));
  }
  return res;
};

$.MVCView$1 = function(key) {
  var t0 = new $.MVCView((void 0), (void 0), (void 0));
  t0.MVCView$1(key);
  return t0;
};

$.contains$2 = function(receiver, other, startIndex) {
  if (!(typeof receiver === 'string')) {
    return receiver.contains$2(other, startIndex);
  }
  $.checkNull(other);
  return $.stringContainsUnchecked(receiver, other, startIndex);
};

$.toString = function(value) {
  if (typeof value == "object") {
    if ($.isJsArray(value) === true) {
      return $.collectionToString(value);
    } else {
      return value.toString$0();
    }
  }
  if (value === 0 && (1 / value) < 0) {
    return '-0.0';
  }
  if (value === (void 0)) {
    return 'null';
  }
  if (typeof value == "function") {
    return 'Closure';
  }
  return String(value);
};

$.MultitonControllerExistsError$0 = function() {
  return new $.MultitonControllerExistsError();
};

$.IndexOutOfRangeException$1 = function(_index) {
  return new $.IndexOutOfRangeException(_index);
};

$._lib3_TextTrackEventsImpl$1 = function(_ptr) {
  return new $._TextTrackEventsImpl(_ptr);
};

$.charCodeAt = function(receiver, index) {
  if (typeof receiver === 'string') {
    if (!(typeof index === 'number')) {
      throw $.captureStackTrace($.IllegalArgumentException$1(index));
    }
    if (index < 0) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(index));
    }
    if (index >= receiver.length) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(index));
    }
    return receiver.charCodeAt(index);
  } else {
    return receiver.charCodeAt$1(index);
  }
};

$._lib3_BatteryManagerEventsImpl$1 = function(_ptr) {
  return new $._BatteryManagerEventsImpl(_ptr);
};

$._lib3_WebSocketEventsImpl$1 = function(_ptr) {
  return new $._WebSocketEventsImpl(_ptr);
};

$.removeLast = function(receiver) {
  if ($.isJsArray(receiver) === true) {
    $.checkGrowable(receiver, 'removeLast');
    if ($.get$length(receiver) === 0) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(-1));
    }
    return receiver.pop();
  }
  return receiver.removeLast$0();
};

$.collectionToString = function(c) {
  var result = $.StringBufferImpl$1('');
  $._emitCollection(c, result, $.List((void 0)));
  return result.toString$0();
};

$.MetaInfo$3 = function(tag, tags, set) {
  return new $.MetaInfo(set, tags, tag);
};

$._lib3_MediaStreamEventsImpl$1 = function(_ptr) {
  return new $._MediaStreamEventsImpl(_ptr);
};

$.defineProperty = function(obj, property, value) {
  Object.defineProperty(obj, property,
      {value: value, enumerable: false, writable: false, configurable: true});;
};

$.dynamicFunction = function(name$) {
  var f = (Object.prototype[name$]);
  if (!(f === (void 0)) && (!!f.methods)) {
    return f.methods;
  }
  var methods = ({});
  var dartMethod = (Object.getPrototypeOf($.CTC8)[name$]);
  if (!(dartMethod === (void 0))) {
    methods['Object'] = dartMethod;
  }
  var bind = (function() {return $.dynamicBind.$call$4(this, name$, methods, Array.prototype.slice.call(arguments));});
  bind.methods = methods;
  $.defineProperty((Object.prototype), name$, bind);
  return methods;
};

$.print = function(obj) {
  return $.printString($.toString(obj));
};

$.checkString = function(value) {
  if (!(typeof value === 'string')) {
    $.checkNull(value);
    throw $.captureStackTrace($.IllegalArgumentException$1(value));
  }
  return value;
};

$.div = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a / b;
  }
  return a.operator$div$1(b);
};

$.addAll = function(receiver, collection) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.addAll$1(collection);
  }
  var iterator = $.iterator(collection);
  for (; iterator.hasNext$0() === true; ) {
    $.add$1(receiver, iterator.next$0());
  }
};

$.objectToString = function(object) {
  var name$ = (object.constructor.name);
  if (name$ === (void 0)) {
    var name0 = (object.constructor.toString().match(/^\s*function\s*\$?(\S*)\s*\(/)[1]);
  } else {
    name0 = name$;
    if ($.charCodeAt(name$, 0) === 36) {
      name0 = $.substring$1(name$, 1);
    }
  }
  return 'Instance of \'' + $.stringToString(name0) + '\'';
};

$._firstProbe = function(hashCode, length$) {
  return $.and(hashCode, $.sub(length$, 1));
};

$.indexOf = function(a, element, startIndex, endIndex) {
  if (typeof a !== 'string' && (typeof a !== 'object'||a.constructor !== Array)) return $.indexOf$bailout(a, element, startIndex, endIndex,  0);
  if (typeof endIndex !== 'number') return $.indexOf$bailout(a, element, startIndex, endIndex,  0);
  if ($.geB(startIndex, a.length)) {
    return -1;
  }
  var startIndex0 = startIndex;
  if ($.ltB(startIndex, 0)) {
    startIndex0 = 0;
  }
  if (typeof startIndex0 !== 'number') return $.indexOf$bailout(a, element, startIndex, endIndex, 3, a, endIndex, startIndex0);
  for (var i = startIndex0; i < endIndex; i = i + 1) {
    if (i !== (i | 0)) throw $.iae(i);
    var t0 = a.length;
    if (i < 0 || i >= t0) throw $.ioore(i);
    if ($.eqB(a[i], element)) {
      return i;
    }
  }
  return -1;
};

$.ioore = function(index) {
  throw $.captureStackTrace($.IndexOutOfRangeException$1(index));
};

$.set$length = function(receiver, newLength) {
  if ($.isJsArray(receiver) === true) {
    $.checkNull(newLength);
    if (!((typeof newLength === 'number') && (newLength === (newLength | 0)))) {
      throw $.captureStackTrace($.IllegalArgumentException$1(newLength));
    }
    if (newLength < 0) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(newLength));
    }
    $.checkGrowable(receiver, 'set length');
    receiver.length = newLength;
  } else {
    receiver.set$length(newLength);
  }
  return newLength;
};

$.indexOf2 = function(a, element, startIndex, endIndex) {
  if (typeof a !== 'string' && (typeof a !== 'object'||a.constructor !== Array)) return $.indexOf2$bailout(a, element, startIndex, endIndex,  0);
  if (typeof endIndex !== 'number') return $.indexOf2$bailout(a, element, startIndex, endIndex,  0);
  if ($.geB(startIndex, a.length)) {
    return -1;
  }
  var startIndex0 = startIndex;
  if ($.ltB(startIndex, 0)) {
    startIndex0 = 0;
  }
  if (typeof startIndex0 !== 'number') return $.indexOf2$bailout(a, element, startIndex, endIndex, 3, a, endIndex, startIndex0);
  for (var i = startIndex0; i < endIndex; i = i + 1) {
    if (i !== (i | 0)) throw $.iae(i);
    var t0 = a.length;
    if (i < 0 || i >= t0) throw $.ioore(i);
    if ($.eqB(a[i], element)) {
      return i;
    }
  }
  return -1;
};

$.typeNameInFirefox = function(obj) {
  var name$ = $.constructorNameFallback(obj);
  if ($.eqB(name$, 'Window')) {
    return 'DOMWindow';
  }
  if ($.eqB(name$, 'Document')) {
    return 'HTMLDocument';
  }
  if ($.eqB(name$, 'XMLDocument')) {
    return 'Document';
  }
  if ($.eqB(name$, 'WorkerMessageEvent')) {
    return 'MessageEvent';
  }
  return name$;
};

$.hashCode = function(receiver) {
  if (typeof receiver === 'number') {
    return receiver & 0x1FFFFFFF;
  }
  if (!(typeof receiver === 'string')) {
    return receiver.hashCode$0();
  }
  var length$ = (receiver.length);
  for (var hash = 0, i = 0; i < length$; i = i0) {
    var hash0 = 536870911 & hash + (receiver.charCodeAt(i));
    var hash1 = 536870911 & hash0 + (524287 & hash0 << 10);
    hash = hash1 ^ $.shr(hash1, 6);
    var i0 = i + 1;
  }
  var hash2 = 536870911 & hash + (67108863 & hash << 3);
  var hash3 = hash2 ^ $.shr(hash2, 11);
  return 536870911 & hash3 + (16383 & hash3 << 15);
};

$.startsWith = function(receiver, other) {
  if (!(typeof receiver === 'string')) {
    return receiver.startsWith$1(other);
  }
  $.checkString(other);
  var length$ = $.get$length(other);
  if ($.gtB(length$, receiver.length)) {
    return false;
  }
  return other == receiver.substring(0, length$);
};

$.TextProxy$0 = function() {
  var t0 = $.NAME2;
  var t1 = new $.TextProxy((void 0), t0, (void 0));
  t1.MVCNotifier$0();
  t1.MVCProxy$2(t0, (void 0));
  t1.TextProxy$0();
  return t1;
};

$.forEach = function(receiver, f) {
  if (!($.isJsArray(receiver) === true)) {
    return receiver.forEach$1(f);
  } else {
    return $.forEach2(receiver, f);
  }
};

$.toStringForNativeObject = function(obj) {
  return 'Instance of ' + $.stringToString($.getTypeNameOf(obj));
};

$.forEach2 = function(iterable, f) {
  for (var t0 = $.iterator(iterable); t0.hasNext$0() === true; ) {
    f.$call$1(t0.next$0());
  }
};

$.dynamicBind = function(obj, name$, methods, arguments$) {
  var tag = $.getTypeNameOf(obj);
  var method = (methods[tag]);
  var method0 = method;
  if (method === (void 0) && !($._dynamicMetadata2() === (void 0))) {
    for (var method1 = method, i = 0; method0 = method1, $.ltB(i, $.get$length($._dynamicMetadata2())); i = i0) {
      var entry = $.index($._dynamicMetadata2(), i);
      if ($.contains$1(entry.get$set(), tag) === true) {
        var method2 = (methods[entry.get$tag()]);
        if (!(method2 === (void 0))) {
          method0 = method2;
          break;
        }
        method1 = method2;
      }
      var i0 = i + 1;
    }
  }
  var method3 = method0;
  if (method0 === (void 0)) {
    method3 = (methods['Object']);
  }
  var proto = (Object.getPrototypeOf(obj));
  var method4 = method3;
  if (method3 === (void 0)) {
    method4 = (function () {if (Object.getPrototypeOf(this) === proto) {$.throwNoSuchMethod.$call$3(this, name$, Array.prototype.slice.call(arguments));} else {return Object.prototype[name$].apply(this, arguments);}});
  }
  var nullCheckMethod = (function() {var res = method4.apply(this, Array.prototype.slice.call(arguments));return res === null ? (void 0) : res;});
  if (!proto.hasOwnProperty(name$)) {
    $.defineProperty(proto, name$, nullCheckMethod);
  }
  return nullCheckMethod.apply(obj, arguments$);
};

$._lib3_MessagePortEventsImpl$1 = function(_ptr) {
  return new $._MessagePortEventsImpl(_ptr);
};

$.getFunctionForTypeNameOf = function() {
  if (!((typeof(navigator)) === 'object')) {
    return $.typeNameInChrome;
  }
  var userAgent = (navigator.userAgent);
  if ($.contains$1(userAgent, $.CTC7) === true) {
    return $.typeNameInChrome;
  } else {
    if ($.contains$1(userAgent, 'Firefox') === true) {
      return $.typeNameInFirefox;
    } else {
      if ($.contains$1(userAgent, 'MSIE') === true) {
        return $.typeNameInIE;
      } else {
        return $.constructorNameFallback;
      }
    }
  }
};

$.index = function(a, index) {
  if (typeof a === 'string' || $.isJsArray(a) === true) {
    if (!((typeof index === 'number') && (index === (index | 0)))) {
      if (!(typeof index === 'number')) {
        throw $.captureStackTrace($.IllegalArgumentException$1(index));
      }
      if (!($.truncate(index) === index)) {
        throw $.captureStackTrace($.IllegalArgumentException$1(index));
      }
    }
    if ($.ltB(index, 0) || $.geB(index, $.get$length(a))) {
      throw $.captureStackTrace($.IndexOutOfRangeException$1(index));
    }
    return a[index];
  }
  return a.operator$index$1(index);
};

$._lib3_ElementEventsImpl$1 = function(_ptr) {
  return new $._ElementEventsImpl(_ptr);
};

$.toLowerCase = function(receiver) {
  if (!(typeof receiver === 'string')) {
    return receiver.toLowerCase$0();
  }
  return receiver.toLowerCase();
};

$.forEach3 = function(iterable, f) {
  for (var t0 = $.iterator(iterable); t0.hasNext$0() === true; ) {
    f.$call$1(t0.next$0());
  }
};

$.List = function(length$) {
  return $.newList(length$);
};

$._isPowerOfTwo = function(x) {
  return $.eq($.and(x, $.sub(x, 1)), 0);
};

$._lib3_XMLHttpRequestUploadEventsImpl$1 = function(_ptr) {
  return new $._XMLHttpRequestUploadEventsImpl(_ptr);
};

$.captureStackTrace = function(ex) {
  var jsError = (new Error());
  jsError.dartException = ex;
  jsError.toString = $.toStringWrapper.$call$0;
  return jsError;
};

$.StackOverflowException$0 = function() {
  return new $.StackOverflowException();
};

$.eq = function(a, b) {
  if (typeof a === "object") {
    if (!!a.operator$eq$1) {
      return a.operator$eq$1(b);
    } else {
      return a === b;
    }
  }
  return a === b;
};

$.StringBufferImpl$1 = function(content$) {
  var t0 = new $.StringBufferImpl((void 0), (void 0));
  t0.StringBufferImpl$1(content$);
  return t0;
};

$.HashMapImplementation$0 = function() {
  var t0 = new $.HashMapImplementation((void 0), (void 0), (void 0), (void 0), (void 0));
  t0.HashMapImplementation$0();
  return t0;
};

$.substring$1 = function(receiver, startIndex) {
  if (!(typeof receiver === 'string')) {
    return receiver.substring$1(startIndex);
  }
  return $.substring$2(receiver, startIndex, (void 0));
};

$.getInstance = function(key) {
  if ($.eqNullB(key) || $.eqB(key, '')) {
    return;
  }
  if ($.eqNullB($.instanceMap)) {
    $.instanceMap = $.HashMapImplementation$0();
  }
  if ($.eqNullB($.index($.instanceMap, key))) {
    $.indexSet($.instanceMap, key, $.MVCFacade$1(key));
  }
  return $.index($.instanceMap, key);
};

$.getInstance2 = function(key) {
  if ($.eqNullB(key) || $.eqB(key, '')) {
    return;
  }
  if ($.eqNullB($.instanceMap2)) {
    $.instanceMap2 = $.HashMapImplementation$0();
  }
  if ($.eqNullB($.index($.instanceMap2, key))) {
    $.indexSet($.instanceMap2, key, $.MVCView$1(key));
  }
  return $.index($.instanceMap2, key);
};

$.getInstance3 = function(key) {
  if ($.eqNullB(key) || $.eqB(key, '')) {
    return;
  }
  if ($.eqNullB($.instanceMap3)) {
    $.instanceMap3 = $.HashMapImplementation$0();
  }
  if ($.eqNullB($.index($.instanceMap3, key))) {
    $.indexSet($.instanceMap3, key, $.MVCController$1(key));
  }
  return $.index($.instanceMap3, key);
};

$._lib3_SharedWorkerContextEventsImpl$1 = function(_ptr) {
  return new $._SharedWorkerContextEventsImpl(_ptr);
};

$.getInstance4 = function(key) {
  if ($.eqNullB(key) || $.eqB(key, '')) {
    return;
  }
  if ($.eqNullB($.instanceMap4)) {
    $.instanceMap4 = $.HashMapImplementation$0();
  }
  if ($.eqNullB($.index($.instanceMap4, key))) {
    $.indexSet($.instanceMap4, key, $.MVCModel$1(key));
  }
  return $.index($.instanceMap4, key);
};

$._lib3_IDBVersionChangeRequestEventsImpl$1 = function(_ptr) {
  return new $._IDBVersionChangeRequestEventsImpl(_ptr);
};

$.gtB = function(a, b) {
  return $.gt(a, b) === true;
};

$.setRuntimeTypeInfo = function(target, typeInfo) {
  if (!(target === (void 0))) {
    target.builtin$typeInfo = typeInfo;
  }
};

$.document = function() {
  return document;;
};

$._lib3_FileWriterEventsImpl$1 = function(_ptr) {
  return new $._FileWriterEventsImpl(_ptr);
};

$.NoSuchMethodException$4 = function(_receiver, _functionName, _arguments, _existingArgumentNames) {
  return new $.NoSuchMethodException(_existingArgumentNames, _arguments, _functionName, _receiver);
};

$.lt = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a < b;
  }
  return a.operator$lt$1(b);
};

$.unwrapException = function(ex) {
  if ("dartException" in ex) {
    return ex.dartException;
  } else {
    if (ex instanceof TypeError) {
      var type = (ex.type);
      var name$ = $.index((ex.arguments), 0);
      if (type === 'property_not_function' || type === 'called_non_callable' || type === 'non_object_property_call' || type === 'non_object_property_load') {
        if (!(name$ === (void 0)) && $.startsWith(name$, '$call$') === true) {
          return $.ObjectNotClosureException$0();
        } else {
          return $.NullPointerException$2((void 0), $.CTC);
        }
      } else {
        if (type === 'undefined_method') {
          if (typeof name$ === 'string' && $.startsWith(name$, '$call$') === true) {
            return $.ObjectNotClosureException$0();
          } else {
            return $.NoSuchMethodException$4('', name$, [], (void 0));
          }
        }
      }
    } else {
      if (ex instanceof RangeError) {
        if ($.contains$1((ex.message), 'call stack') === true) {
          return $.StackOverflowException$0();
        }
      }
    }
  }
  return ex;
};

$.ceil = function(receiver) {
  if (!(typeof receiver === 'number')) {
    return receiver.ceil$0();
  }
  return Math.ceil(receiver);
};

$.getTypeNameOf = function(obj) {
  if ($._getTypeNameOf === (void 0)) {
    $._getTypeNameOf = $.getFunctionForTypeNameOf();
  }
  return $._getTypeNameOf.$call$1(obj);
};

$.sub = function(a, b) {
  if ($.checkNumbers(a, b) === true) {
    return a - b;
  }
  return a.operator$sub$1(b);
};

$.allMatchesInStringUnchecked$bailout = function(needle, haystack, state, env0, env1, env2) {
  switch (state) {
    case 1:
      length$ = env0;
      result = env1;
      patternLength = env2;
      break;
  }
  switch (state) {
    case 0:
      var result = $.List((void 0));
      $.setRuntimeTypeInfo(result, ({E: 'Match'}));
      var length$ = $.get$length(haystack);
      var patternLength = $.get$length(needle);
    case 1:
      state = 0;
      var startIndex = 0;
      L0: while (true) {
        if (!true) break L0;
        var position = $.indexOf$2(haystack, needle, startIndex);
        if ($.eqB(position, -1)) {
          break;
        }
        result.push($.StringMatch$3(position, haystack, needle));
        var endIndex = $.add(position, patternLength);
        if ($.eqB(endIndex, length$)) {
          break;
        } else {
          if ($.eqB(position, endIndex)) {
            startIndex = $.add(startIndex, 1);
          } else {
            startIndex = endIndex;
          }
        }
      }
      return result;
  }
};

$.getRange2$bailout = function(a, start, length$, accumulator, state, env0, env1) {
  switch (state) {
    case 1:
      t0 = env0;
      break;
    case 2:
      t0 = env0;
      i = env1;
      break;
  }
  switch (state) {
    case 0:
    case 1:
      state = 0;
    case 2:
      state = 0;
      if ($.ltB(length$, 0)) {
        throw $.captureStackTrace($.IllegalArgumentException$1('length'));
      }
      if ($.ltB(start, 0)) {
        throw $.captureStackTrace($.IndexOutOfRangeException$1(start));
      }
      var end = $.add(start, length$);
      if ($.gtB(end, $.get$length(a))) {
        throw $.captureStackTrace($.IndexOutOfRangeException$1(end));
      }
      var i0 = start;
      L0: while (true) {
        if (!$.ltB(i0, end)) break L0;
        $.add$1(accumulator, $.index(a, i0));
        i0 = $.add(i0, 1);
      }
      return accumulator;
  }
};

$.indexOf2$bailout = function(a, element, startIndex, endIndex, state, env0, env1, env2) {
  switch (state) {
    case 1:
      t0 = env0;
      break;
    case 2:
      t0 = env0;
      t1 = env1;
      break;
    case 3:
      t0 = env0;
      t1 = env1;
      startIndex0 = env2;
      break;
  }
  switch (state) {
    case 0:
    case 1:
      state = 0;
    case 2:
      state = 0;
      if ($.geB(startIndex, $.get$length(a))) {
        return -1;
      }
      var startIndex0 = startIndex;
      if ($.ltB(startIndex, 0)) {
        startIndex0 = 0;
      }
    case 3:
      state = 0;
      var i = startIndex0;
      L0: while (true) {
        if (!$.ltB(i, endIndex)) break L0;
        if ($.eqB($.index(a, i), element)) {
          return i;
        }
        i = $.add(i, 1);
      }
      return -1;
  }
};

$.indexOf$bailout = function(a, element, startIndex, endIndex, state, env0, env1, env2) {
  switch (state) {
    case 1:
      t0 = env0;
      break;
    case 2:
      t0 = env0;
      t1 = env1;
      break;
    case 3:
      t0 = env0;
      t1 = env1;
      startIndex0 = env2;
      break;
  }
  switch (state) {
    case 0:
    case 1:
      state = 0;
    case 2:
      state = 0;
      if ($.geB(startIndex, $.get$length(a))) {
        return -1;
      }
      var startIndex0 = startIndex;
      if ($.ltB(startIndex, 0)) {
        startIndex0 = 0;
      }
    case 3:
      state = 0;
      var i = startIndex0;
      L0: while (true) {
        if (!$.ltB(i, endIndex)) break L0;
        if ($.eqB($.index(a, i), element)) {
          return i;
        }
        i = $.add(i, 1);
      }
      return -1;
  }
};

$.buildDynamicMetadata$bailout = function(inputTable, state, env0, env1, env2, env3, env4, env5, env6) {
  switch (state) {
    case 1:
      t0 = env0;
      break;
    case 2:
      t0 = env0;
      result = env1;
      tag = env2;
      i = env3;
      tags = env4;
      set = env5;
      tagNames = env6;
      break;
  }
  switch (state) {
    case 0:
    case 1:
      state = 0;
      var result = [];
      var i = 0;
    case 2:
      L0: while (true) {
        switch (state) {
          case 0:
            if (!$.ltB(i, $.get$length(inputTable))) break L0;
            var tag = $.index($.index(inputTable, i), 0);
            var tags = $.index($.index(inputTable, i), 1);
            var set = $.HashSetImplementation$0();
            $.setRuntimeTypeInfo(set, ({E: 'String'}));
            var tagNames = $.split(tags, '|');
          case 2:
            state = 0;
            var j = 0;
            L1: while (true) {
              if (!$.ltB(j, $.get$length(tagNames))) break L1;
              set.add$1($.index(tagNames, j));
              j = j + 1;
            }
            $.add$1(result, $.MetaInfo$3(tag, tags, set));
            i = i + 1;
        }
      }
      return result;
  }
};

$.dynamicBind.$call$4 = $.dynamicBind;
$.throwNoSuchMethod.$call$3 = $.throwNoSuchMethod;
$.typeNameInIE.$call$1 = $.typeNameInIE;
$.typeNameInChrome.$call$1 = $.typeNameInChrome;
$.toStringWrapper.$call$0 = $.toStringWrapper;
$.invokeClosure.$call$5 = $.invokeClosure;
$.typeNameInFirefox.$call$1 = $.typeNameInFirefox;
$.constructorNameFallback.$call$1 = $.constructorNameFallback;
Isolate.$finishClasses();
$.makeConstantList = function(list) {
  list.immutable$list = true;
  list.fixed$length = true;
  return list;
};
$.CTC = Isolate.prototype.makeConstantList([]);
$.CTC7 = new Isolate.prototype.JSSyntaxRegExp(false, false, 'Chrome|DumpRenderTree');
$.CTC2 = new Isolate.prototype._DeletedKeySentinel();
$.CTC5 = new Isolate.prototype.IllegalArgumentException('Invalid list length');
$.CTC4 = new Isolate.prototype.UnsupportedOperationException('');
$.CTC3 = new Isolate.prototype.NoMoreElementsException();
$.CTC8 = new Isolate.prototype.Object();
$.CTC6 = new Isolate.prototype.JSSyntaxRegExp(false, false, '^#[_a-zA-Z]\\w*$');
var $ = new Isolate();
(function() {
$.defineProperty(Object.prototype, 'is$Collection', function() { return false; });
$.defineProperty(Object.prototype, 'is$List2', function() { return false; });
$.defineProperty(Object.prototype, 'is$Element', function() { return false; });
$.defineProperty(Object.prototype, 'is$Map', function() { return false; });
$.defineProperty(Object.prototype, 'toString$0', function() { return $.toStringForNativeObject(this); });
$.dynamicFunction('is$Element').SVGRadialGradientElement = function() { return true; };
$.dynamicFunction('get$name').DocumentType = function() { return this.name; };
$.dynamicFunction('$dom_dispatchEvent$1').WebSocket = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').WebSocket = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').WebSocket = function() {
  return $._lib3_WebSocketEventsImpl$1(this);
 };
$.dynamicFunction('get$type').SVGFETurbulenceElement = function() { return this.type; };
$.dynamicFunction('is$Element').SVGFETurbulenceElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLDListElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFETileElement = function() { return true; };
$.dynamicFunction('set$value').HTMLOutputElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLOutputElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLOutputElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLOutputElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLOutputElement = function() { return true; };
$.dynamicFunction('set$value').SVGNumber = function(v) { this.value = v; };
$.dynamicFunction('get$value').SVGNumber = function() { return this.value; };
$.dynamicFunction('getRange$2').Int8Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Int8Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Int8Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Int8Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Int8Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Int8Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Int8Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Int8Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Int8Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Int8Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Int8Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Int8Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Int8Array = function() { return this.length; };
$.dynamicFunction('is$List2').Int8Array = function() { return true; };
$.dynamicFunction('is$Collection').Int8Array = function() { return true; };
$.dynamicFunction('is$Element').HTMLOptGroupElement = function() { return true; };
$.dynamicFunction('get$userAgent').WorkerNavigator = function() { return this.userAgent; };
$.dynamicFunction('get$name').HTMLAppletElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLAppletElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEBlendElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLTableCaptionElement = function() { return true; };
$.dynamicFunction('set$value').HTMLLIElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLLIElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLLIElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLLIElement = function() { return true; };
$.dynamicFunction('set$innerHTML').ShadowRoot = function(v) { this.innerHTML = v; };
$.dynamicFunction('is$Element').ShadowRoot = function() { return true; };
$.dynamicFunction('is$Element').HTMLQuoteElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLMenuElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLHeadElement = function() { return true; };
$.dynamicFunction('get$length').SQLResultSetRowList = function() { return this.length; };
$.dynamicFunction('filter$1').NodeIterator = function(arg0) { return this.filter.$call$1(arg0); };
$.dynamicFunction('get$length').CSSRuleList = function() { return this.length; };
$.dynamicFunction('getRange$2').Uint8Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Uint8Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Uint8Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Uint8Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Uint8Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Uint8Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Uint8Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Uint8Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Uint8Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Uint8Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Uint8Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Uint8Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Uint8Array = function() { return this.length; };
$.dynamicFunction('is$List2').Uint8Array = function() { return true; };
$.dynamicFunction('is$Collection').Uint8Array = function() { return true; };
$.dynamicFunction('get$name').DOMFileSystem = function() { return this.name; };
$.dynamicFunction('get$length').CSSValueList = function() { return this.length; };
$.dynamicFunction('is$Element').SVGGElement = function() { return true; };
$.dynamicFunction('is$Element').SVGAnimateMotionElement = function() { return true; };
$.dynamicFunction('is$Element').SVGTRefElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLBaseElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEGaussianBlurElement = function() { return true; };
$.dynamicFunction('get$type').SVGStyleElement = function() { return this.type; };
$.dynamicFunction('is$Element').SVGStyleElement = function() { return true; };
$.dynamicFunction('get$name').DOMPlugin = function() { return this.name; };
$.dynamicFunction('get$length').DOMPlugin = function() { return this.length; };
$.dynamicFunction('$dom_dispatchEvent$1').MediaStream = function(event) {
  return this.dispatchEvent(event);
 };
$.dynamicFunction('$dom_addEventListener$3').MediaStream = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').MediaStream = function() {
  return $._lib3_MediaStreamEventsImpl$1(this);
 };
$.dynamicFunction('get$name').WebKitAnimation = function() { return this.name; };
$.dynamicFunction('get$length').SpeechRecognitionResult = function() { return this.length; };
$.dynamicFunction('$dom_dispatchEvent$1').SpeechRecognition = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').SpeechRecognition = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').SpeechRecognition = function() {
  return $._lib3_SpeechRecognitionEventsImpl$1(this);
 };
$.dynamicFunction('set$value').SVGLength = function(v) { this.value = v; };
$.dynamicFunction('get$value').SVGLength = function() { return this.value; };
$.dynamicFunction('$dom_dispatchEvent$1').MessagePort = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').MessagePort = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').MessagePort = function() {
  return $._lib3_MessagePortEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGImageElement = function() { return true; };
$.dynamicFunction('get$length').EntryArraySync = function() { return this.length; };
$.dynamicFunction('is$Element').SVGFEFuncGElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFontFaceElement = function() { return true; };
$.dynamicFunction('toString$0').IDBDatabaseException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').IDBDatabaseException = function() { return this.name; };
$.dynamicFunction('get$tag').Notification = function() { return this.tag; };
$.dynamicFunction('get$on').Notification = function() {
  return $._lib3_NotificationEventsImpl$1(this);
 };
$.dynamicFunction('$dom_dispatchEvent$1').WorkerContext = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').WorkerContext = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$navigator').WorkerContext = function() { return this.navigator; };
$.dynamicFunction('get$on').WorkerContext = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$on')) {
    return $._lib3_WorkerContextEventsImpl$1(this);
  } else {
    return Object.prototype.get$on.call(this);
  }
 };
$.dynamicFunction('is$Element').HTMLTableCellElement = function() { return true; };
$.dynamicFunction('set$value').HTMLInputElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLInputElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLInputElement = function() { return this.type; };
$.dynamicFunction('get$pattern').HTMLInputElement = function() { return this.pattern; };
$.dynamicFunction('get$name').HTMLInputElement = function() { return this.name; };
$.dynamicFunction('get$checked').HTMLInputElement = function() { return this.checked; };
$.dynamicFunction('get$on').HTMLInputElement = function() {
  return $._lib3_InputElementEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLInputElement = function() { return true; };
$.dynamicFunction('get$length').TextTrackCueList = function() { return this.length; };
$.dynamicFunction('get$type').HTMLFieldSetElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLFieldSetElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLFieldSetElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEDropShadowElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').EventTarget = function(event) {
  if (Object.getPrototypeOf(this).hasOwnProperty('$dom_dispatchEvent$1')) {
    return this.dispatchEvent(event);
  } else {
    return Object.prototype.$dom_dispatchEvent$1.call(this, event);
  }
 };
$.dynamicFunction('$dom_addEventListener$3').EventTarget = function(type, listener, useCapture) {
  if (Object.getPrototypeOf(this).hasOwnProperty('$dom_addEventListener$3')) {
    return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
  } else {
    return Object.prototype.$dom_addEventListener$3.call(this, type, listener, useCapture);
  }
 };
$.dynamicFunction('get$on').EventTarget = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$on')) {
    return $._lib3_EventsImpl$1(this);
  } else {
    return Object.prototype.get$on.call(this);
  }
 };
$.dynamicFunction('getRange$2').HTMLCollection = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').HTMLCollection = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').HTMLCollection = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').HTMLCollection = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').HTMLCollection = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').HTMLCollection = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').HTMLCollection = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').HTMLCollection = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').HTMLCollection = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').HTMLCollection = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'Node'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').HTMLCollection = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').HTMLCollection = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').HTMLCollection = function() { return this.length; };
$.dynamicFunction('is$List2').HTMLCollection = function() { return true; };
$.dynamicFunction('is$Collection').HTMLCollection = function() { return true; };
$.dynamicFunction('is$Element').SVGAnimateColorElement = function() { return true; };
$.dynamicFunction('get$type').DataTransferItem = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLTableColElement = function() { return true; };
$.dynamicFunction('get$length').ClientRectList = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLAudioElement = function() { return true; };
$.dynamicFunction('get$type').SVGScriptElement = function() { return this.type; };
$.dynamicFunction('is$Element').SVGScriptElement = function() { return true; };
$.dynamicFunction('is$Element').SVGMarkerElement = function() { return true; };
$.dynamicFunction('is$Element').SVGLineElement = function() { return true; };
$.dynamicFunction('getRange$2').Int16Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Int16Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Int16Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Int16Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Int16Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Int16Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Int16Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Int16Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Int16Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Int16Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Int16Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Int16Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Int16Array = function() { return this.length; };
$.dynamicFunction('is$List2').Int16Array = function() { return true; };
$.dynamicFunction('is$Collection').Int16Array = function() { return true; };
$.dynamicFunction('is$Element').SVGMaskElement = function() { return true; };
$.dynamicFunction('set$value').HTMLButtonElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLButtonElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLButtonElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLButtonElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLButtonElement = function() { return true; };
$.dynamicFunction('set$innerHTML').SVGElement = function(svg) {
  var container = $.Element$tag('div');
  container.set$innerHTML('<svg version="1.1">' + $.stringToString(svg) + '</svg>');
  this.set$elements(container.get$elements().get$first().get$elements());
 };
$.dynamicFunction('set$elements').SVGElement = function(value) {
  var elements = this.get$elements();
  $.clear(elements);
  $.addAll(elements, value);
 };
$.dynamicFunction('get$elements').SVGElement = function() {
  return $.FilteredElementList$1(this);
 };
$.dynamicFunction('is$Element').SVGElement = function() { return true; };
$.dynamicFunction('filter$1').TreeWalker = function(arg0) { return this.filter.$call$1(arg0); };
$.dynamicFunction('is$Element').SVGFEPointLightElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEMergeNodeElement = function() { return true; };
$.dynamicFunction('get$type').HTMLLinkElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLLinkElement = function() { return true; };
$.dynamicFunction('is$Element').SVGAnimationElement = function() { return true; };
$.dynamicFunction('getRange$2').Float32Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Float32Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Float32Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Float32Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Float32Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Float32Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Float32Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Float32Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Float32Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Float32Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'num'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Float32Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Float32Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Float32Array = function() { return this.length; };
$.dynamicFunction('is$List2').Float32Array = function() { return true; };
$.dynamicFunction('is$Collection').Float32Array = function() { return true; };
$.dynamicFunction('is$Element').SVGFEImageElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').FileReader = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').FileReader = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').FileReader = function() {
  return $._lib3_FileReaderEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGFilterElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLHRElement = function() { return true; };
$.dynamicFunction('get$length').SpeechInputResultList = function() { return this.length; };
$.dynamicFunction('is$Element').SVGFEConvolveMatrixElement = function() { return true; };
$.dynamicFunction('getRange$2').MediaList = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').MediaList = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').MediaList = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').MediaList = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').MediaList = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').MediaList = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').MediaList = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').MediaList = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').MediaList = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').MediaList = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'String'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').MediaList = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').MediaList = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').MediaList = function() { return this.length; };
$.dynamicFunction('is$List2').MediaList = function() { return true; };
$.dynamicFunction('is$Collection').MediaList = function() { return true; };
$.dynamicFunction('is$Element').HTMLSpanElement = function() { return true; };
$.dynamicFunction('toString$0').SVGException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').SVGException = function() { return this.name; };
$.dynamicFunction('is$Element').SVGAElement = function() { return true; };
$.dynamicFunction('toString$0').DOMSelection = function() {
  return this.toString();
 };
$.dynamicFunction('get$type').DOMSelection = function() { return this.type; };
$.dynamicFunction('is$Element').SVGAltGlyphDefElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEMergeElement = function() { return true; };
$.dynamicFunction('is$Element').SVGTextPathElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLTableSectionElement = function() { return true; };
$.dynamicFunction('get$type').HTMLScriptElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLScriptElement = function() { return true; };
$.dynamicFunction('$dom_replaceChild$2').Node = function(newChild, oldChild) {
  return this.replaceChild(newChild,oldChild);
 };
$.dynamicFunction('$dom_removeChild$1').Node = function(oldChild) {
  return this.removeChild(oldChild);
 };
$.dynamicFunction('contains$1').Node = function(other) {
  return this.contains(other);
 };
$.dynamicFunction('$dom_appendChild$1').Node = function(newChild) {
  return this.appendChild(newChild);
 };
$.dynamicFunction('set$text').Node = function(value) {
  this.textContent = value;;
 };
$.dynamicFunction('get$parent').Node = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$parent')) {
    return this.parentNode;;
  } else {
    return Object.prototype.get$parent.call(this);
  }
 };
$.dynamicFunction('get$$dom_childNodes').Node = function() {
  return this.childNodes;;
 };
$.dynamicFunction('replaceWith$1').Node = function(otherNode) {
  try {
    var parent$ = this.get$parent();
    parent$.$dom_replaceChild$2(otherNode, this);
}  catch (t0) {
    $.unwrapException(t0);
  }
  return this;
 };
$.dynamicFunction('remove$0').Node = function() {
  if (!$.eqNullB(this.get$parent())) {
    this.get$parent().$dom_removeChild$1(this);
  }
  return this;
 };
$.dynamicFunction('get$nodes').Node = function() {
  return $._lib3_ChildNodeListLazy$1(this);
 };
$.dynamicFunction('get$name').IDBIndex = function() { return this.name; };
$.dynamicFunction('is$Element').SVGTextPositioningElement = function() { return true; };
$.dynamicFunction('toString$0').OperationNotAllowedException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').OperationNotAllowedException = function() { return this.name; };
$.dynamicFunction('get$length').FileWriterSync = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLLegendElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLContentElement = function() { return true; };
$.dynamicFunction('get$type').MutationRecord = function() { return this.type; };
$.dynamicFunction('is$Element').SVGFontFaceUriElement = function() { return true; };
$.dynamicFunction('query$1').DocumentFragment = function(selectors) {
  return this.querySelector(selectors);
 };
$.dynamicFunction('get$on').DocumentFragment = function() {
  return $._lib3_ElementEventsImpl$1(this);
 };
$.dynamicFunction('click$0').DocumentFragment = function() {
 };
$.dynamicFunction('get$click').DocumentFragment = function() { return new $.Closure23(this); };
$.dynamicFunction('get$parent').DocumentFragment = function() {
  return;
 };
$.dynamicFunction('get$$dom_lastElementChild').DocumentFragment = function() {
  return $.last(this.get$elements());
 };
$.dynamicFunction('get$$dom_firstElementChild').DocumentFragment = function() {
  return this.get$elements().first$0();
 };
$.dynamicFunction('set$innerHTML').DocumentFragment = function(value) {
  if (Object.getPrototypeOf(this).hasOwnProperty('set$innerHTML')) {
    $.clear(this.get$nodes());
  var e = $.Element$tag('div');
  e.set$innerHTML(value);
  var nodes = $.List$from(e.get$nodes());
  $.addAll(this.get$nodes(), nodes);
  } else {
    return Object.prototype.set$innerHTML.call(this, value);
  }
 };
$.dynamicFunction('get$elements').DocumentFragment = function() {
  if ($.eqNullB(this.get$_lib3_elements())) {
    this.set$_lib3_elements($.FilteredElementList$1(this));
  }
  return this.get$_lib3_elements();
 };
$.dynamicFunction('set$_lib3_elements').DocumentFragment = function(v) { this._lib3_elements = v; };
$.dynamicFunction('get$_lib3_elements').DocumentFragment = function() { return this._lib3_elements; };
$.dynamicFunction('is$Element').DocumentFragment = function() { return true; };
$.dynamicFunction('get$length').MediaStreamList = function() { return this.length; };
$.dynamicFunction('is$Element').SVGFontFaceFormatElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLTrackElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').FileWriter = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').FileWriter = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$length').FileWriter = function() { return this.length; };
$.dynamicFunction('get$on').FileWriter = function() {
  return $._lib3_FileWriterEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGFEOffsetElement = function() { return true; };
$.dynamicFunction('get$type').Blob = function() { return this.type; };
$.dynamicFunction('$dom_dispatchEvent$1').IDBRequest = function(evt) {
  if (Object.getPrototypeOf(this).hasOwnProperty('$dom_dispatchEvent$1')) {
    return this.dispatchEvent(evt);
  } else {
    return Object.prototype.$dom_dispatchEvent$1.call(this, evt);
  }
 };
$.dynamicFunction('$dom_addEventListener$3').IDBRequest = function(type, listener, useCapture) {
  if (Object.getPrototypeOf(this).hasOwnProperty('$dom_addEventListener$3')) {
    return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
  } else {
    return Object.prototype.$dom_addEventListener$3.call(this, type, listener, useCapture);
  }
 };
$.dynamicFunction('get$on').IDBRequest = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$on')) {
    return $._lib3_IDBRequestEventsImpl$1(this);
  } else {
    return Object.prototype.get$on.call(this);
  }
 };
$.dynamicFunction('get$name').WebKitCSSKeyframesRule = function() { return this.name; };
$.dynamicFunction('set$value').AudioParam = function(v) { this.value = v; };
$.dynamicFunction('get$value').AudioParam = function() { return this.value; };
$.dynamicFunction('get$name').AudioParam = function() { return this.name; };
$.dynamicFunction('set$value').Attr = function(v) { this.value = v; };
$.dynamicFunction('get$value').Attr = function() { return this.value; };
$.dynamicFunction('get$name').Attr = function() { return this.name; };
$.dynamicFunction('get$length').History = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLUnknownElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEDiffuseLightingElement = function() { return true; };
$.dynamicFunction('is$Element').SVGSetElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').TextTrackList = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').TextTrackList = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$length').TextTrackList = function() { return this.length; };
$.dynamicFunction('get$on').TextTrackList = function() {
  return $._lib3_TextTrackListEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGViewElement = function() { return true; };
$.dynamicFunction('toString$0').XMLHttpRequestException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').XMLHttpRequestException = function() { return this.name; };
$.dynamicFunction('clear$0').SVGNumberList = function() {
  return this.clear();
 };
$.dynamicFunction('toString$0').WorkerLocation = function() {
  return this.toString();
 };
$.dynamicFunction('get$type').SVGFEColorMatrixElement = function() { return this.type; };
$.dynamicFunction('is$Element').SVGFEColorMatrixElement = function() { return true; };
$.dynamicFunction('is$Element').SVGPolylineElement = function() { return true; };
$.dynamicFunction('get$name').HTMLMapElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLMapElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLDirectoryElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').XMLHttpRequest = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').XMLHttpRequest = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').XMLHttpRequest = function() {
  return $._lib3_XMLHttpRequestEventsImpl$1(this);
 };
$.dynamicFunction('get$type').SVGComponentTransferFunctionElement = function() { return this.type; };
$.dynamicFunction('is$Element').SVGComponentTransferFunctionElement = function() { return true; };
$.dynamicFunction('is$Element').SVGClipPathElement = function() { return true; };
$.dynamicFunction('get$length').SpeechGrammarList = function() { return this.length; };
$.dynamicFunction('clear$0').SVGPathSegList = function() {
  return this.clear();
 };
$.dynamicFunction('is$Element').SVGForeignObjectElement = function() { return true; };
$.dynamicFunction('getRange$2').StyleSheetList = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').StyleSheetList = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').StyleSheetList = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').StyleSheetList = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').StyleSheetList = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').StyleSheetList = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').StyleSheetList = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').StyleSheetList = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').StyleSheetList = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').StyleSheetList = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'StyleSheet'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').StyleSheetList = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').StyleSheetList = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').StyleSheetList = function() { return this.length; };
$.dynamicFunction('is$List2').StyleSheetList = function() { return true; };
$.dynamicFunction('is$Collection').StyleSheetList = function() { return true; };
$.dynamicFunction('get$type').HTMLEmbedElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLEmbedElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLEmbedElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEMorphologyElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEFuncAElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLCanvasElement = function() { return true; };
$.dynamicFunction('get$name').HTMLFormElement = function() { return this.name; };
$.dynamicFunction('get$length').HTMLFormElement = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLFormElement = function() { return true; };
$.dynamicFunction('toString$0').EventException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').EventException = function() { return this.name; };
$.dynamicFunction('is$Element').SVGVKernElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').DOMApplicationCache = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').DOMApplicationCache = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').DOMApplicationCache = function() {
  return $._lib3_DOMApplicationCacheEventsImpl$1(this);
 };
$.dynamicFunction('get$type').HTMLObjectElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLObjectElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLObjectElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').IDBTransaction = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').IDBTransaction = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').IDBTransaction = function() {
  return $._lib3_IDBTransactionEventsImpl$1(this);
 };
$.dynamicFunction('$dom_dispatchEvent$1').EventSource = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').EventSource = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').EventSource = function() {
  return $._lib3_EventSourceEventsImpl$1(this);
 };
$.dynamicFunction('get$length').WebKitAnimationList = function() { return this.length; };
$.dynamicFunction('is$Element').SVGFEDisplacementMapElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').DOMWindow = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').DOMWindow = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$navigator').DOMWindow = function() { return this.navigator; };
$.dynamicFunction('get$name').DOMWindow = function() { return this.name; };
$.dynamicFunction('get$length').DOMWindow = function() { return this.length; };
$.dynamicFunction('get$on').DOMWindow = function() {
  return $._lib3_WindowEventsImpl$1(this);
 };
$.dynamicFunction('get$type').Oscillator = function() { return this.type; };
$.dynamicFunction('set$value').HTMLMeterElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLMeterElement = function() { return this.value; };
$.dynamicFunction('is$Element').HTMLMeterElement = function() { return true; };
$.dynamicFunction('toString$0').WebKitCSSMatrix = function() {
  return this.toString();
 };
$.dynamicFunction('get$length').HTMLAllCollection = function() { return this.length; };
$.dynamicFunction('$dom_createEvent$1').SVGDocument = function(eventType) {
  return this.createEvent(eventType);
 };
$.dynamicFunction('is$Element').SVGDocument = function() { return true; };
$.dynamicFunction('remove$0').EntrySync = function() {
  return this.remove();
 };
$.dynamicFunction('get$name').EntrySync = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLAreaElement = function() { return true; };
$.dynamicFunction('is$Element').SVGUseElement = function() { return true; };
$.dynamicFunction('is$Element').SVGGradientElement = function() { return true; };
$.dynamicFunction('get$name').HTMLMetaElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLMetaElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').JavaScriptAudioNode = function(event) {
  return this.dispatchEvent(event);
 };
$.dynamicFunction('$dom_addEventListener$3').JavaScriptAudioNode = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').JavaScriptAudioNode = function() {
  return $._lib3_JavaScriptAudioNodeEventsImpl$1(this);
 };
$.dynamicFunction('get$userAgent').Navigator = function() { return this.userAgent; };
$.dynamicFunction('is$Element').SVGPolygonElement = function() { return true; };
$.dynamicFunction('is$Element').SVGSymbolElement = function() { return true; };
$.dynamicFunction('getRange$2').Uint32Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Uint32Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Uint32Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Uint32Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Uint32Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Uint32Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Uint32Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Uint32Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Uint32Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Uint32Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Uint32Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Uint32Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Uint32Array = function() { return this.length; };
$.dynamicFunction('is$List2').Uint32Array = function() { return true; };
$.dynamicFunction('is$Collection').Uint32Array = function() { return true; };
$.dynamicFunction('is$Element').SVGStopElement = function() { return true; };
$.dynamicFunction('toString$0').RangeException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').RangeException = function() { return this.name; };
$.dynamicFunction('set$value').HTMLProgressElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLProgressElement = function() { return this.value; };
$.dynamicFunction('is$Element').HTMLProgressElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').MediaController = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').MediaController = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('is$Element').HTMLTableElement = function() { return true; };
$.dynamicFunction('is$Element').SVGRectElement = function() { return true; };
$.dynamicFunction('toString$0').Range = function() {
  return this.toString();
 };
$.dynamicFunction('getRange$2').Uint16Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Uint16Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Uint16Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Uint16Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Uint16Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Uint16Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Uint16Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Uint16Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Uint16Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Uint16Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Uint16Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Uint16Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Uint16Array = function() { return this.length; };
$.dynamicFunction('is$List2').Uint16Array = function() { return true; };
$.dynamicFunction('is$Collection').Uint16Array = function() { return true; };
$.dynamicFunction('is$Element').HTMLFontElement = function() { return true; };
$.dynamicFunction('is$Element').SVGCircleElement = function() { return true; };
$.dynamicFunction('is$Element').SVGCursorElement = function() { return true; };
$.dynamicFunction('$dom_querySelector$1').HTMLDocument = function(selectors) {
  return this.querySelector(selectors);;
 };
$.dynamicFunction('query$1').HTMLDocument = function(selectors) {
  if ($.CTC6.hasMatch$1(selectors) === true) {
    return this.$dom_getElementById$1($.substring$1(selectors, 1));
  }
  return this.$dom_querySelector$1(selectors);
 };
$.dynamicFunction('$dom_getElementById$1').HTMLDocument = function(elementId) {
  return this.getElementById(elementId);
 };
$.dynamicFunction('$dom_createEvent$1').HTMLDocument = function(eventType) {
  if (Object.getPrototypeOf(this).hasOwnProperty('$dom_createEvent$1')) {
    return this.createEvent(eventType);
  } else {
    return Object.prototype.$dom_createEvent$1.call(this, eventType);
  }
 };
$.dynamicFunction('get$body').HTMLDocument = function() { return this.body; };
$.dynamicFunction('get$on').HTMLDocument = function() {
  return $._lib3_DocumentEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLDocument = function() { return true; };
$.dynamicFunction('is$Element').SVGFESpotLightElement = function() { return true; };
$.dynamicFunction('get$type').StyleMedia = function() { return this.type; };
$.dynamicFunction('is$Element').SVGAltGlyphElement = function() { return true; };
$.dynamicFunction('is$Element').SVGMetadataElement = function() { return true; };
$.dynamicFunction('get$length').DOMPluginArray = function() { return this.length; };
$.dynamicFunction('get$type').HTMLOListElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLOListElement = function() { return true; };
$.dynamicFunction('set$value').HTMLParamElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLParamElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLParamElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLParamElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLParamElement = function() { return true; };
$.dynamicFunction('set$value').HTMLTextAreaElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLTextAreaElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLTextAreaElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLTextAreaElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLTextAreaElement = function() { return true; };
$.dynamicFunction('get$type').JavaScriptCallFrame = function() { return this.type; };
$.dynamicFunction('is$Element').SVGHKernElement = function() { return true; };
$.dynamicFunction('is$Element').SVGTitleElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLPreElement = function() { return true; };
$.dynamicFunction('get$type').HTMLUListElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLUListElement = function() { return true; };
$.dynamicFunction('getRange$2').Float64Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Float64Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Float64Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Float64Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Float64Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Float64Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Float64Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Float64Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Float64Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Float64Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'num'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Float64Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Float64Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Float64Array = function() { return this.length; };
$.dynamicFunction('is$List2').Float64Array = function() { return true; };
$.dynamicFunction('is$Collection').Float64Array = function() { return true; };
$.dynamicFunction('get$type').CSSRule = function() { return this.type; };
$.dynamicFunction('getRange$2').Int32Array = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').Int32Array = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').Int32Array = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').Int32Array = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').Int32Array = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').Int32Array = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').Int32Array = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').Int32Array = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').Int32Array = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').Int32Array = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'int'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').Int32Array = function(index, value) {
  this[index] = value;
 };
$.dynamicFunction('operator$index$1').Int32Array = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').Int32Array = function() { return this.length; };
$.dynamicFunction('is$List2').Int32Array = function() { return true; };
$.dynamicFunction('is$Collection').Int32Array = function() { return true; };
$.dynamicFunction('contains$1').DOMStringList = function(string) {
  return this.contains(string);
 };
$.dynamicFunction('getRange$2').DOMStringList = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').DOMStringList = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').DOMStringList = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').DOMStringList = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').DOMStringList = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').DOMStringList = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').DOMStringList = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').DOMStringList = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').DOMStringList = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').DOMStringList = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'String'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').DOMStringList = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').DOMStringList = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').DOMStringList = function() { return this.length; };
$.dynamicFunction('is$List2').DOMStringList = function() { return true; };
$.dynamicFunction('is$Collection').DOMStringList = function() { return true; };
$.dynamicFunction('getRange$2').NamedNodeMap = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').NamedNodeMap = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').NamedNodeMap = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').NamedNodeMap = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').NamedNodeMap = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').NamedNodeMap = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').NamedNodeMap = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').NamedNodeMap = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').NamedNodeMap = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').NamedNodeMap = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'Node'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').NamedNodeMap = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').NamedNodeMap = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').NamedNodeMap = function() { return this.length; };
$.dynamicFunction('is$List2').NamedNodeMap = function() { return true; };
$.dynamicFunction('is$Collection').NamedNodeMap = function() { return true; };
$.dynamicFunction('toString$0').XPathException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').XPathException = function() { return this.name; };
$.dynamicFunction('get$length').MediaStreamTrackList = function() { return this.length; };
$.dynamicFunction('toString$0').HTMLAnchorElement = function() {
  return this.toString();
 };
$.dynamicFunction('get$type').HTMLAnchorElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLAnchorElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLAnchorElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEFloodElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLModElement = function() { return true; };
$.dynamicFunction('get$length').DOMMimeTypeArray = function() { return this.length; };
$.dynamicFunction('is$Element').SVGPathElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLBaseFontElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFECompositeElement = function() { return true; };
$.dynamicFunction('is$Element').SVGAltGlyphItemElement = function() { return true; };
$.dynamicFunction('is$Element').SVGSwitchElement = function() { return true; };
$.dynamicFunction('get$value').IDBCursorWithValue = function() { return this.value; };
$.dynamicFunction('get$type').HTMLKeygenElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLKeygenElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLKeygenElement = function() { return true; };
$.dynamicFunction('get$type').StyleSheet = function() { return this.type; };
$.dynamicFunction('$dom_dispatchEvent$1').AbstractWorker = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').AbstractWorker = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').AbstractWorker = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$on')) {
    return $._lib3_AbstractWorkerEventsImpl$1(this);
  } else {
    return Object.prototype.get$on.call(this);
  }
 };
$.dynamicFunction('get$name').Entry = function() { return this.name; };
$.dynamicFunction('clear$0').SVGStringList = function() {
  return this.clear();
 };
$.dynamicFunction('is$Element').SVGSVGElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFESpecularLightingElement = function() { return true; };
$.dynamicFunction('is$Element').SVGMissingGlyphElement = function() { return true; };
$.dynamicFunction('is$Element').SVGAnimateTransformElement = function() { return true; };
$.dynamicFunction('query$1').Element = function(selectors) {
  return this.querySelector(selectors);
 };
$.dynamicFunction('click$0').Element = function() {
  return this.click();
 };
$.dynamicFunction('get$click').Element = function() { return new $.Closure24(this); };
$.dynamicFunction('get$$dom_lastElementChild').Element = function() {
  return this.lastElementChild;;
 };
$.dynamicFunction('set$innerHTML').Element = function(v) { this.innerHTML = v; };
$.dynamicFunction('get$$dom_firstElementChild').Element = function() {
  return this.firstElementChild;;
 };
$.dynamicFunction('get$$dom_children').Element = function() {
  return this.children;;
 };
$.dynamicFunction('get$on').Element = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$on')) {
    return $._lib3_ElementEventsImpl$1(this);
  } else {
    return Object.prototype.get$on.call(this);
  }
 };
$.dynamicFunction('get$elements').Element = function() {
  if (Object.getPrototypeOf(this).hasOwnProperty('get$elements')) {
    return $._lib3_ChildrenElementList$_wrap$1(this);
  } else {
    return Object.prototype.get$elements.call(this);
  }
 };
$.dynamicFunction('set$elements').Element = function(value) {
  if (Object.getPrototypeOf(this).hasOwnProperty('set$elements')) {
    var elements = this.get$elements();
  $.clear(elements);
  $.addAll(elements, value);
  } else {
    return Object.prototype.set$elements.call(this, value);
  }
 };
$.dynamicFunction('is$Element').Element = function() { return true; };
$.dynamicFunction('is$Element').SVGDescElement = function() { return true; };
$.dynamicFunction('get$length').FileList = function() { return this.length; };
$.dynamicFunction('set$value').DOMSettableTokenList = function(v) { this.value = v; };
$.dynamicFunction('get$value').DOMSettableTokenList = function() { return this.value; };
$.dynamicFunction('is$Element').SVGTSpanElement = function() { return true; };
$.dynamicFunction('get$length').AudioBuffer = function() { return this.length; };
$.dynamicFunction('get$filter').CSSStyleDeclaration = function() {
  return this.getPropertyValue$1('' + $.stringToString($._browserPrefix()) + 'filter');
 };
$.dynamicFunction('filter$1').CSSStyleDeclaration = function(arg0) { return this.get$filter().$call$1(arg0); };
$.dynamicFunction('get$clear').CSSStyleDeclaration = function() {
  return this.getPropertyValue$1('clear');
 };
$.dynamicFunction('clear$0').CSSStyleDeclaration = function() { return this.get$clear().$call$0(); };
$.dynamicFunction('getPropertyValue$1').CSSStyleDeclaration = function(propertyName) {
  return this.getPropertyValue(propertyName);
 };
$.dynamicFunction('get$length').CSSStyleDeclaration = function() { return this.length; };
$.dynamicFunction('is$Element').SVGGlyphRefElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEComponentTransferElement = function() { return true; };
$.dynamicFunction('$dom_setItem$2').Storage = function(key, data) {
  return this.setItem(key,data);
 };
$.dynamicFunction('$dom_key$1').Storage = function(index) {
  return this.key(index);
 };
$.dynamicFunction('$dom_getItem$1').Storage = function(key) {
  return this.getItem(key);
 };
$.dynamicFunction('$dom_clear$0').Storage = function() {
  return this.clear();
 };
$.dynamicFunction('get$$dom_length').Storage = function() {
  return this.length;;
 };
$.dynamicFunction('isEmpty$0').Storage = function() {
  return $.eqNull(this.$dom_key$1(0));
 };
$.dynamicFunction('get$length').Storage = function() {
  return this.get$$dom_length();
 };
$.dynamicFunction('forEach$1').Storage = function(f) {
  for (var i = 0; true; i = i + 1) {
    var key = this.$dom_key$1(i);
    if ($.eqNullB(key)) {
      return;
    }
    f.$call$2(key, this.operator$index$1(key));
  }
 };
$.dynamicFunction('clear$0').Storage = function() {
  return this.$dom_clear$0();
 };
$.dynamicFunction('operator$indexSet$2').Storage = function(key, value) {
  return this.$dom_setItem$2(key, value);
 };
$.dynamicFunction('operator$index$1').Storage = function(key) {
  return this.$dom_getItem$1(key);
 };
$.dynamicFunction('containsKey$1').Storage = function(key) {
  return !$.eqNullB(this.$dom_getItem$1(key));
 };
$.dynamicFunction('is$Map').Storage = function() { return true; };
$.dynamicFunction('get$type').HTMLStyleElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLStyleElement = function() { return true; };
$.dynamicFunction('get$on').DedicatedWorkerContext = function() {
  return $._lib3_DedicatedWorkerContextEventsImpl$1(this);
 };
$.dynamicFunction('clear$0').HTMLBRElement = function() { return this.clear.$call$0(); };
$.dynamicFunction('is$Element').HTMLBRElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFEFuncRElement = function() { return true; };
$.dynamicFunction('get$on').Worker = function() {
  return $._lib3_WorkerEventsImpl$1(this);
 };
$.dynamicFunction('clear$0').SVGPointList = function() {
  return this.clear();
 };
$.dynamicFunction('clear$0').SVGTransformList = function() {
  return this.clear();
 };
$.dynamicFunction('$dom_dispatchEvent$1').TextTrack = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').TextTrack = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').TextTrack = function() {
  return $._lib3_TextTrackEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGFEDistantLightElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLLabelElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLMarqueeElement = function() { return true; };
$.dynamicFunction('clear$0').SVGLengthList = function() {
  return this.clear();
 };
$.dynamicFunction('get$name').DOMFileSystemSync = function() { return this.name; };
$.dynamicFunction('query$1').NodeSelector = function(selectors) {
  return this.querySelector(selectors);
 };
$.dynamicFunction('is$Element').SVGEllipseElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').BatteryManager = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').BatteryManager = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').BatteryManager = function() {
  return $._lib3_BatteryManagerEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGAnimateElement = function() { return true; };
$.dynamicFunction('is$Element').SVGTextContentElement = function() { return true; };
$.dynamicFunction('get$length').SVGElementInstanceList = function() { return this.length; };
$.dynamicFunction('get$length').SpeechRecognitionResultList = function() { return this.length; };
$.dynamicFunction('get$type').BiquadFilterNode = function() { return this.type; };
$.dynamicFunction('get$on').AudioContext = function() {
  return $._lib3_AudioContextEventsImpl$1(this);
 };
$.dynamicFunction('getRange$2').TouchList = function(start, rangeLength) {
  return $.getRange2(this, start, rangeLength, []);
 };
$.dynamicFunction('removeLast$0').TouchList = function() {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot removeLast on immutable List.'));
 };
$.dynamicFunction('last$0').TouchList = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').TouchList = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').TouchList = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').TouchList = function(f) {
  return $.filter3(this, [], f);
 };
$.dynamicFunction('forEach$1').TouchList = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('addAll$1').TouchList = function(collection) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('add$1').TouchList = function(value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot add to immutable List.'));
 };
$.dynamicFunction('iterator$0').TouchList = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'Touch'}));
  return t0;
 };
$.dynamicFunction('operator$indexSet$2').TouchList = function(index, value) {
  throw $.captureStackTrace($.UnsupportedOperationException$1('Cannot assign element of immutable List.'));
 };
$.dynamicFunction('operator$index$1').TouchList = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').TouchList = function() { return this.length; };
$.dynamicFunction('is$List2').TouchList = function() { return true; };
$.dynamicFunction('is$Collection').TouchList = function() { return true; };
$.dynamicFunction('get$on').HTMLFrameSetElement = function() {
  return $._lib3_FrameSetElementEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLFrameSetElement = function() { return true; };
$.dynamicFunction('addEventListener$3').SVGElementInstance = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('addEventListener$2').SVGElementInstance = function(type,listener) {
  listener = $.convertDartClosureToJS(listener);
  return this.addEventListener(type,listener);
};
$.dynamicFunction('get$on').SVGElementInstance = function() {
  return $._lib3_SVGElementInstanceEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGLinearGradientElement = function() { return true; };
$.dynamicFunction('is$Element').SVGFontFaceNameElement = function() { return true; };
$.dynamicFunction('get$name').SharedWorkerContext = function() { return this.name; };
$.dynamicFunction('get$on').SharedWorkerContext = function() {
  return $._lib3_SharedWorkerContextEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGFontFaceSrcElement = function() { return true; };
$.dynamicFunction('toString$0').DOMTokenList = function() {
  return this.toString();
 };
$.dynamicFunction('contains$1').DOMTokenList = function(token) {
  return this.contains(token);
 };
$.dynamicFunction('add$1').DOMTokenList = function(token) {
  return this.add(token);
 };
$.dynamicFunction('get$length').DOMTokenList = function() { return this.length; };
$.dynamicFunction('is$Element').SVGDefsElement = function() { return true; };
$.dynamicFunction('toString$0').Location = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').HTMLFrameElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLFrameElement = function() { return true; };
$.dynamicFunction('preventDefault$0').Event = function() {
  return this.preventDefault();
 };
$.dynamicFunction('$dom_initEvent$3').Event = function(eventTypeArg, canBubbleArg, cancelableArg) {
  return this.initEvent(eventTypeArg,canBubbleArg,cancelableArg);
 };
$.dynamicFunction('get$type').Event = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLVideoElement = function() { return true; };
$.dynamicFunction('get$type').SVGTransform = function() { return this.type; };
$.dynamicFunction('toString$0').FileException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').FileException = function() { return this.name; };
$.dynamicFunction('set$value').HTMLSelectElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLSelectElement = function() { return this.value; };
$.dynamicFunction('get$type').HTMLSelectElement = function() { return this.type; };
$.dynamicFunction('get$name').HTMLSelectElement = function() { return this.name; };
$.dynamicFunction('set$length').HTMLSelectElement = function(v) { this.length = v; };
$.dynamicFunction('get$length').HTMLSelectElement = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLSelectElement = function() { return true; };
$.dynamicFunction('is$Element').SVGGlyphElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLDivElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').TextTrackCue = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').TextTrackCue = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('set$text').TextTrackCue = function(v) { this.text = v; };
$.dynamicFunction('get$on').TextTrackCue = function() {
  return $._lib3_TextTrackCueEventsImpl$1(this);
 };
$.dynamicFunction('get$name').File = function() { return this.name; };
$.dynamicFunction('$dom_dispatchEvent$1').XMLHttpRequestUpload = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').XMLHttpRequestUpload = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').XMLHttpRequestUpload = function() {
  return $._lib3_XMLHttpRequestUploadEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').SVGPatternElement = function() { return true; };
$.dynamicFunction('get$length').CharacterData = function() { return this.length; };
$.dynamicFunction('get$type').PerformanceNavigation = function() { return this.type; };
$.dynamicFunction('get$on').HTMLMediaElement = function() {
  return $._lib3_MediaElementEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLMediaElement = function() { return true; };
$.dynamicFunction('set$value').HTMLOptionElement = function(v) { this.value = v; };
$.dynamicFunction('get$value').HTMLOptionElement = function() { return this.value; };
$.dynamicFunction('is$Element').HTMLOptionElement = function() { return true; };
$.dynamicFunction('get$type').WebGLActiveInfo = function() { return this.type; };
$.dynamicFunction('get$name').WebGLActiveInfo = function() { return this.name; };
$.dynamicFunction('get$length').EntryArray = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLDetailsElement = function() { return true; };
$.dynamicFunction('get$type').DOMMimeType = function() { return this.type; };
$.dynamicFunction('clear$0').DataTransferItemList = function() {
  return this.clear();
 };
$.dynamicFunction('add$2').DataTransferItemList = function(data_OR_file, type) {
  return this.add(data_OR_file,type);
 };
$.dynamicFunction('add$1').DataTransferItemList = function(data_OR_file) {
  return this.add(data_OR_file);
};
$.dynamicFunction('get$length').DataTransferItemList = function() { return this.length; };
_ConsoleImpl = (typeof console == 'undefined' ? {} : console);
$.dynamicFunction('is$Element').SVGFEFuncBElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').DeprecatedPeerConnection = function(event) {
  return this.dispatchEvent(event);
 };
$.dynamicFunction('$dom_addEventListener$3').DeprecatedPeerConnection = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').DeprecatedPeerConnection = function() {
  return $._lib3_DeprecatedPeerConnectionEventsImpl$1(this);
 };
$.dynamicFunction('get$name').HTMLImageElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLImageElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').IDBVersionChangeRequest = function(event) {
  return this.dispatchEvent(event);
 };
$.dynamicFunction('$dom_addEventListener$3').IDBVersionChangeRequest = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').IDBVersionChangeRequest = function() {
  return $._lib3_IDBVersionChangeRequestEventsImpl$1(this);
 };
$.dynamicFunction('get$name').HTMLIFrameElement = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLIFrameElement = function() { return true; };
$.dynamicFunction('toString$0').DOMException = function() {
  return this.toString();
 };
$.dynamicFunction('get$name').DOMException = function() { return this.name; };
$.dynamicFunction('get$length').TimeRanges = function() { return this.length; };
$.dynamicFunction('is$Element').HTMLHeadingElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').PeerConnection00 = function(event) {
  return this.dispatchEvent(event);
 };
$.dynamicFunction('$dom_addEventListener$3').PeerConnection00 = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$on').PeerConnection00 = function() {
  return $._lib3_PeerConnection00EventsImpl$1(this);
 };
$.dynamicFunction('get$type').HTMLSourceElement = function() { return this.type; };
$.dynamicFunction('is$Element').HTMLSourceElement = function() { return true; };
$.dynamicFunction('$dom_dispatchEvent$1').IDBDatabase = function(evt) {
  return this.dispatchEvent(evt);
 };
$.dynamicFunction('$dom_addEventListener$3').IDBDatabase = function(type, listener, useCapture) {
  return this.addEventListener(type,$.convertDartClosureToJS(listener),useCapture);
 };
$.dynamicFunction('get$name').IDBDatabase = function() { return this.name; };
$.dynamicFunction('get$on').IDBDatabase = function() {
  return $._lib3_IDBDatabaseEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLTableRowElement = function() { return true; };
$.dynamicFunction('set$value').SVGAngle = function(v) { this.value = v; };
$.dynamicFunction('get$value').SVGAngle = function() { return this.value; };
$.dynamicFunction('is$Element').SVGFontElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLHtmlElement = function() { return true; };
$.dynamicFunction('is$Element').SVGTextElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLTitleElement = function() { return true; };
$.dynamicFunction('clear$0').IDBObjectStore = function() {
  return this.clear();
 };
$.dynamicFunction('add$2').IDBObjectStore = function(value, key) {
  return this.add(value,key);
 };
$.dynamicFunction('add$1').IDBObjectStore = function(value) {
  return this.add(value);
};
$.dynamicFunction('get$name').IDBObjectStore = function() { return this.name; };
$.dynamicFunction('is$Element').HTMLShadowElement = function() { return true; };
$.dynamicFunction('set$length').HTMLOptionsCollection = function(value) {
  this.length = value;;
 };
$.dynamicFunction('get$length').HTMLOptionsCollection = function() {
  return this.length;;
 };
$.dynamicFunction('is$List2').HTMLOptionsCollection = function() { return true; };
$.dynamicFunction('is$Collection').HTMLOptionsCollection = function() { return true; };
$.dynamicFunction('operator$index$1').NodeList = function(index) {
  return this[index];;
 };
$.dynamicFunction('get$length').NodeList = function() { return this.length; };
$.dynamicFunction('getRange$2').NodeList = function(start, rangeLength) {
  return $._lib3_NodeListWrapper$1($.getRange2(this, start, rangeLength, []));
 };
$.dynamicFunction('get$first').NodeList = function() {
  return this.operator$index$1(0);
 };
$.dynamicFunction('first$0').NodeList = function() { return this.get$first().$call$0(); };
$.dynamicFunction('last$0').NodeList = function() {
  return this.operator$index$1($.sub($.get$length(this), 1));
 };
$.dynamicFunction('indexOf$2').NodeList = function(element, start) {
  return $.indexOf2(this, element, start, $.get$length(this));
 };
$.dynamicFunction('isEmpty$0').NodeList = function() {
  return $.eq($.get$length(this), 0);
 };
$.dynamicFunction('filter$1').NodeList = function(f) {
  return $._lib3_NodeListWrapper$1($.filter3(this, [], f));
 };
$.dynamicFunction('forEach$1').NodeList = function(f) {
  return $.forEach3(this, f);
 };
$.dynamicFunction('operator$indexSet$2').NodeList = function(index, value) {
  this.get$_lib3_parent().$dom_replaceChild$2(value, this.operator$index$1(index));
 };
$.dynamicFunction('clear$0').NodeList = function() {
  this.get$_lib3_parent().set$text('');
 };
$.dynamicFunction('removeLast$0').NodeList = function() {
  var result = this.last$0();
  if (!$.eqNullB(result)) {
    this.get$_lib3_parent().$dom_removeChild$1(result);
  }
  return result;
 };
$.dynamicFunction('addAll$1').NodeList = function(collection) {
  for (var t0 = $.iterator(collection); t0.hasNext$0() === true; ) {
    var t1 = t0.next$0();
    this.get$_lib3_parent().$dom_appendChild$1(t1);
  }
 };
$.dynamicFunction('add$1').NodeList = function(value) {
  this.get$_lib3_parent().$dom_appendChild$1(value);
 };
$.dynamicFunction('iterator$0').NodeList = function() {
  var t0 = $._lib3_FixedSizeListIterator$1(this);
  $.setRuntimeTypeInfo(t0, ({T: 'Node'}));
  return t0;
 };
$.dynamicFunction('get$_lib3_parent').NodeList = function() { return this._lib3_parent; };
$.dynamicFunction('is$List2').NodeList = function() { return true; };
$.dynamicFunction('is$Collection').NodeList = function() { return true; };
$.dynamicFunction('get$on').HTMLBodyElement = function() {
  return $._lib3_BodyElementEventsImpl$1(this);
 };
$.dynamicFunction('is$Element').HTMLBodyElement = function() { return true; };
$.dynamicFunction('is$Element').HTMLParagraphElement = function() { return true; };
$.dynamicFunction('is$List2').Uint8ClampedArray = function() { return true; };
$.dynamicFunction('is$Collection').Uint8ClampedArray = function() { return true; };
$.dynamicFunction('is$Element').SVGMPathElement = function() { return true; };
// 294 dynamic classes.
// 355 classes
// 31 !leaf
(function(){
  var v0/*class(_SVGTextPositioningElementImpl)*/ = 'SVGTextPositioningElement|SVGTextElement|SVGTSpanElement|SVGTRefElement|SVGAltGlyphElement';
  var v1/*class(_SVGTextContentElementImpl)*/ = [v0/*class(_SVGTextPositioningElementImpl)*/,'SVGTextContentElement|SVGTextPathElement'].join('|');
  var v2/*class(_SVGGradientElementImpl)*/ = 'SVGGradientElement|SVGRadialGradientElement|SVGLinearGradientElement';
  var v3/*class(_SVGComponentTransferFunctionElementImpl)*/ = 'SVGComponentTransferFunctionElement|SVGFEFuncRElement|SVGFEFuncGElement|SVGFEFuncBElement|SVGFEFuncAElement';
  var v4/*class(_SVGAnimationElementImpl)*/ = 'SVGAnimationElement|SVGSetElement|SVGAnimateTransformElement|SVGAnimateMotionElement|SVGAnimateElement|SVGAnimateColorElement';
  var v5/*class(_SVGElementImpl)*/ = [v1/*class(_SVGTextContentElementImpl)*/,v2/*class(_SVGGradientElementImpl)*/,v3/*class(_SVGComponentTransferFunctionElementImpl)*/,v4/*class(_SVGAnimationElementImpl)*/,'SVGElement|SVGViewElement|SVGVKernElement|SVGUseElement|SVGTitleElement|SVGSymbolElement|SVGSwitchElement|SVGStyleElement|SVGStopElement|SVGScriptElement|SVGSVGElement|SVGRectElement|SVGPolylineElement|SVGPolygonElement|SVGPatternElement|SVGPathElement|SVGMissingGlyphElement|SVGMetadataElement|SVGMaskElement|SVGMarkerElement|SVGMPathElement|SVGLineElement|SVGImageElement|SVGHKernElement|SVGGlyphRefElement|SVGGlyphElement|SVGGElement|SVGForeignObjectElement|SVGFontFaceUriElement|SVGFontFaceSrcElement|SVGFontFaceNameElement|SVGFontFaceFormatElement|SVGFontFaceElement|SVGFontElement|SVGFilterElement|SVGFETurbulenceElement|SVGFETileElement|SVGFESpotLightElement|SVGFESpecularLightingElement|SVGFEPointLightElement|SVGFEOffsetElement|SVGFEMorphologyElement|SVGFEMergeNodeElement|SVGFEMergeElement|SVGFEImageElement|SVGFEGaussianBlurElement|SVGFEFloodElement|SVGFEDropShadowElement|SVGFEDistantLightElement|SVGFEDisplacementMapElement|SVGFEDiffuseLightingElement|SVGFEConvolveMatrixElement|SVGFECompositeElement|SVGFEComponentTransferElement|SVGFEColorMatrixElement|SVGFEBlendElement|SVGEllipseElement|SVGDescElement|SVGDefsElement|SVGCursorElement|SVGClipPathElement|SVGCircleElement|SVGAltGlyphItemElement|SVGAltGlyphDefElement|SVGAElement'].join('|');
  var v6/*class(_MediaElementImpl)*/ = 'HTMLMediaElement|HTMLVideoElement|HTMLAudioElement';
  var v7/*class(_ElementImpl)*/ = [v5/*class(_SVGElementImpl)*/,v6/*class(_MediaElementImpl)*/,'Element|HTMLUnknownElement|HTMLUListElement|HTMLTrackElement|HTMLTitleElement|HTMLTextAreaElement|HTMLTableSectionElement|HTMLTableRowElement|HTMLTableElement|HTMLTableColElement|HTMLTableCellElement|HTMLTableCaptionElement|HTMLStyleElement|HTMLSpanElement|HTMLSourceElement|HTMLShadowElement|HTMLSelectElement|HTMLScriptElement|HTMLQuoteElement|HTMLProgressElement|HTMLPreElement|HTMLParamElement|HTMLParagraphElement|HTMLOutputElement|HTMLOptionElement|HTMLOptGroupElement|HTMLObjectElement|HTMLOListElement|HTMLModElement|HTMLMeterElement|HTMLMetaElement|HTMLMenuElement|HTMLMarqueeElement|HTMLMapElement|HTMLLinkElement|HTMLLegendElement|HTMLLabelElement|HTMLLIElement|HTMLKeygenElement|HTMLInputElement|HTMLImageElement|HTMLIFrameElement|HTMLHtmlElement|HTMLHeadingElement|HTMLHeadElement|HTMLHRElement|HTMLFrameSetElement|HTMLFrameElement|HTMLFormElement|HTMLFontElement|HTMLFieldSetElement|HTMLEmbedElement|HTMLDivElement|HTMLDirectoryElement|HTMLDetailsElement|HTMLDListElement|HTMLContentElement|HTMLCanvasElement|HTMLButtonElement|HTMLBodyElement|HTMLBaseFontElement|HTMLBaseElement|HTMLBRElement|HTMLAreaElement|HTMLAppletElement|HTMLAnchorElement|HTMLElement'].join('|');
  var v8/*class(_DocumentFragmentImpl)*/ = 'DocumentFragment|ShadowRoot';
  var v9/*class(_DocumentImpl)*/ = 'HTMLDocument|SVGDocument';
  var v10/*class(_CharacterDataImpl)*/ = 'CharacterData|Text|CDATASection|Comment';
  var v11/*class(_WorkerContextImpl)*/ = 'WorkerContext|SharedWorkerContext|DedicatedWorkerContext';
  var v12/*class(_NodeImpl)*/ = [v7/*class(_ElementImpl)*/,v8/*class(_DocumentFragmentImpl)*/,v9/*class(_DocumentImpl)*/,v10/*class(_CharacterDataImpl)*/,'Node|ProcessingInstruction|Notation|EntityReference|Entity|DocumentType|Attr'].join('|');
  var v13/*class(_MediaStreamImpl)*/ = 'MediaStream|LocalMediaStream';
  var v14/*class(_IDBRequestImpl)*/ = 'IDBRequest|IDBVersionChangeRequest';
  var v15/*class(_AbstractWorkerImpl)*/ = 'AbstractWorker|Worker|SharedWorker';
  var table = [
    // [dynamic-dispatch-tag, tags of classes implementing dynamic-dispatch-tag]
    ['SVGGradientElement', v2/*class(_SVGGradientElementImpl)*/],
    ['Uint8Array', 'Uint8Array|Uint8ClampedArray'],
    ['HTMLDocument', v9/*class(_DocumentImpl)*/],
    ['CSSValueList', 'CSSValueList|WebKitCSSFilterValue|WebKitCSSTransformValue'],
    ['MediaStream', v13/*class(_MediaStreamImpl)*/],
    ['CSSRule', 'CSSRule|WebKitCSSRegionRule|CSSUnknownRule|CSSStyleRule|CSSPageRule|CSSMediaRule|WebKitCSSKeyframesRule|WebKitCSSKeyframeRule|CSSImportRule|CSSFontFaceRule|CSSCharsetRule'],
    ['WorkerContext', v11/*class(_WorkerContextImpl)*/],
    ['SVGTextPositioningElement', v0/*class(_SVGTextPositioningElementImpl)*/],
    ['SVGTextContentElement', v1/*class(_SVGTextContentElementImpl)*/],
    ['SVGComponentTransferFunctionElement', v3/*class(_SVGComponentTransferFunctionElementImpl)*/],
    ['SVGAnimationElement', v4/*class(_SVGAnimationElementImpl)*/],
    ['SVGElement', v5/*class(_SVGElementImpl)*/],
    ['HTMLMediaElement', v6/*class(_MediaElementImpl)*/],
    ['Element', v7/*class(_ElementImpl)*/],
    ['DocumentFragment', v8/*class(_DocumentFragmentImpl)*/],
    ['CharacterData', v10/*class(_CharacterDataImpl)*/],
    ['Node', v12/*class(_NodeImpl)*/],
    ['IDBRequest', v14/*class(_IDBRequestImpl)*/],
    ['AbstractWorker', v15/*class(_AbstractWorkerImpl)*/],
    ['EventTarget', [v11/*class(_WorkerContextImpl)*/,v12/*class(_NodeImpl)*/,v13/*class(_MediaStreamImpl)*/,v14/*class(_IDBRequestImpl)*/,v15/*class(_AbstractWorkerImpl)*/,'EventTarget|XMLHttpRequestUpload|XMLHttpRequest|DOMWindow|WebSocket|TextTrackList|TextTrackCue|TextTrack|SpeechRecognition|PeerConnection00|Notification|MessagePort|MediaController|IDBTransaction|IDBDatabase|FileWriter|FileReader|EventSource|DeprecatedPeerConnection|DOMApplicationCache|BatteryManager|AudioContext'].join('|')],
    ['HTMLCollection', 'HTMLCollection|HTMLOptionsCollection'],
    ['StyleSheet', 'StyleSheet|CSSStyleSheet'],
    ['Entry', 'Entry|FileEntry|DirectoryEntry'],
    ['DOMTokenList', 'DOMTokenList|DOMSettableTokenList'],
    ['Event', 'Event|WebGLContextEvent|UIEvent|WheelEvent|TouchEvent|TextEvent|SVGZoomEvent|MouseEvent|KeyboardEvent|CompositionEvent|WebKitTransitionEvent|TrackEvent|StorageEvent|SpeechRecognitionEvent|SpeechInputEvent|ProgressEvent|XMLHttpRequestProgressEvent|PopStateEvent|PageTransitionEvent|OverflowEvent|OfflineAudioCompletionEvent|MutationEvent|MessageEvent|MediaStreamEvent|MediaKeyEvent|IDBVersionChangeEvent|HashChangeEvent|ErrorEvent|DeviceOrientationEvent|DeviceMotionEvent|CustomEvent|CloseEvent|BeforeLoadEvent|AudioProcessingEvent|WebKitAnimationEvent'],
    ['Blob', 'Blob|File'],
    ['AudioParam', 'AudioParam|AudioGain'],
    ['EntrySync', 'EntrySync|FileEntrySync|DirectoryEntrySync']];
$.dynamicSetMetadata(table);
})();

})();
Isolate.$finishClasses();
if (typeof window != 'undefined' && typeof document != 'undefined' &&
    window.addEventListener && document.readyState == 'loading') {
  window.addEventListener('DOMContentLoaded', function(e) {
    $.main();
  });
} else {
  $.main();
}
function init() {
Isolate.$defineClass = function(cls, superclass, constructor, prototype) {
  Isolate.prototype[cls] = constructor;
  constructor.prototype = prototype;
  if (superclass !== "") {
    Isolate.pendingClasses[cls] = superclass;
  }
};
Isolate.pendingClasses = {};
Isolate.$finishClasses = function() {
  var pendingClasses = Isolate.pendingClasses;
  Isolate.pendingClasses = {};
  var finishedClasses = {};
  function finishClass(cls) {
    if (finishedClasses[cls]) return;
    finishedClasses[cls] = true;
    var superclass = pendingClasses[cls];
    if (!superclass) return;
    finishClass(superclass);
    var constructor = Isolate.prototype[cls];
    var superConstructor = Isolate.prototype[superclass];
    var prototype = constructor.prototype;
    if (prototype.__proto__) {
      prototype.__proto__ = superConstructor.prototype;
      prototype.constructor = constructor;
    } else {
      function tmp() {};
      tmp.prototype = superConstructor.prototype;
      var newPrototype = new tmp();
      constructor.prototype = newPrototype;
      newPrototype.constructor = constructor;
      var hasOwnProperty = Object.prototype.hasOwnProperty;
      for (var member in prototype) {
        if (hasOwnProperty.call(prototype, member)) {
          newPrototype[member] = prototype[member];
        }
      }
    }
  }
  for (var cls in pendingClasses) finishClass(cls);
};
;
}
